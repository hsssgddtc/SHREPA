# _*_ coding: utf-8 _*_

"""
Lianjia_Collection_Main_2017.py by shai
"""

import requests
import random
import urllib2
import pymysql
import re
from bs4 import BeautifulSoup

import utilities
import processor

BASE_URL = "http://sh.lianjia.com"
url_house = "http://sh.lianjia.com/ershoufang/sh4509559.html"
url_community = "http://sh.lianjia.com/xiaoqu/5011000017696.html"

#define the fetch process
class LianjiaFetcher(processor.Fetcher):

    def url_fetch(self, url, keys, critical, fetch_repeat):
        headers = {"User-Agent": utilities.make_random_useragent("pc"), "Accept-Encoding": "gzip"}
        response = requests.get(url, headers=headers, timeout=10)

        content = (response.status_code, response.url, response.text)
        return 1, content


class LianjiaParser(processor.Parser):
    def html_parse(self, content, content_type):
        """
        :param content: 
        :return: 
        """
        url_list, content_dict = [], {}

        cur_code, cur_url, cur_html = content
        bsObj = BeautifulSoup(cur_html, "html.parser")

        if content_type == "main_links":
            for content in bsObj.find_all(name="div", attrs={"id": "plateList"}):
                for item in content.find_all(name="a", gahref=re.compile(
                        "^((?!(district-nolimit)).)*$")):
                    DISTRICT_URL = BASE_URL + item.get("href")
                    print("Current District: " + item.get_text())
                    print(DISTRICT_URL)

                    dis_code, content_dis = fetcher.working(DISTRICT_URL, None, 1, 3)
                    processor.html_parse(content_dis, "district_links")

        elif content_type == "district_links":
            for area_content in bsObj.find_all(name="div", attrs={"class": "level2 gio_plate"}):
                for area_item in area_content.find_all(name="a", gahref=re.compile("^((?!(plate-nolimit)).)*$")):
                    AREA_URL = BASE_URL + area_item.get("href")
                    print("Current Stage: " + area_item.text)
                    cur_code, content = fetcher.working(AREA_URL, None, 1, 3)
                    processor.html_parse(content, "area_links")


        elif content_type == "area_links":
            current_page = bsObj.find_all(name="span", attrs={"class": "current"})[0].text
            print("Current Page: " + str(current_page))

            processor.html_parse(content, "house_links")

            next_content = bsObj.find_all(name="div", attrs={"class": "c-pagination"})[0].find_all(name="a", attrs={
                "gahref": "results_next_page"})

            if next_content <> []:
                next_page = BASE_URL + next_content[0].get("href")
                cur_code, content = fetcher.working(next_page, None, 1, 3)
                processor.html_parse(content, "area_links")
            else:
                exit

        elif content_type == "house_links":
            for i in range(1, 31):
                list_link = "results_click_order_" + str(i)
                if bsObj.find_all(name="a", attrs={"gahref": list_link}) == []:
                    break;

                detail_link = BASE_URL + bsObj.find_all(name="a", attrs={"gahref": list_link})[0].get("href")

                detail_code, content_detail = fetcher.working(detail_link, None, 1, 3)
                house_content_dict = processor.html_parse(content_detail, "house")


                house_content_dict.update({"Hash_Value":str(hash(frozenset(house_content_dict.items())))})

                if house_content_dict.get("Hash_Value") not in cur_house_hash_set:
                    # for keys, values in content_detail_dict.items(): print(keys + " : " + values)
                    dataset = saver.db_prep("house", house_content_dict)
                    saver.db_insert("house", dataset)
                    cur_house_hash_set.add(house_content_dict.get("Hash_Value"))
                    print("House Insert Done~")
                else:
                    print("House Exists")

                # for keys, values in content[2].items(): print(keys + " : " + values)

                url_community = house_content_dict.get("Community_Link")
                #print(url_community)

                cur_code, content = fetcher.working(url_community, None, 1, 3)
                community_content_dict = processor.html_parse(content, "community")

                community_content_dict.update({"Building_Num_on_Total":house_content_dict.pop("Building_Num_on_Total")})
                community_content_dict.update({"House_Num_on_Total": house_content_dict.pop("House_Num_on_Total")})
                community_content_dict.update({"House_Num_on_Sold": house_content_dict.pop("House_Num_on_Sold")})
                community_content_dict.update({"House_Num_on_Rent": house_content_dict.pop("House_Num_on_Rent")})

                if "Gonglue_Link" in community_content_dict:
                    url_community_gonglue = community_content_dict.pop("Gonglue_Link")
                    cur_code, content = fetcher.working(url_community_gonglue, None, 1, 3)

                    community_content_dict = processor.html_parse_com_gonglue(content, community_content_dict)

                community_content_dict.update({"Hash_Value": str(hash(frozenset(community_content_dict.items())))})


                if community_content_dict.get("Hash_Value") not in cur_community_hash_set:
                    dataset = saver.db_prep("community", community_content_dict)
                    saver.db_insert("community", dataset)
                    cur_community_hash_set.add(community_content_dict.get("Hash_Value"))
                    print("Community Insert Done~")
                else:
                    print("Community Exists")



        elif content_type == "house":
            content_dict.update({"House_Title": utilities.get_string_strip(bsObj.find_all(name="div", attrs={"class": "header-row2"})[0].text)})
            content_dict.update({"Listing_Price": utilities.get_string_num(utilities.get_string_strip(bsObj.find_all(name="span", attrs={"class": "price-num"})[0].text)+u"万")})
            content_dict.update(
                {"Quoted_Price": utilities.get_string_num(utilities.get_string_strip(bsObj.find_all(name="p", attrs={"class": "price-unit-num"})[0].find_all(name="span")[0].text))})
            content_dict.update(
                {"Year_Build": utilities.get_string_num(utilities.get_string_strip(bsObj.find_all(name="li", attrs={"class": "main-item u-tr"})[0].find_all(name="p", attrs={
                    "class": "u-fz12"})[
                    0].text))})
            content_dict.update(
                {"Ring_Line":
                     utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(name="span",
                                                                                                             attrs={
                                                                                                                 "class": "item-cell"})[
                         5].text)})
            community_info = \
                utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(name="span", attrs={
                    "class": "item-cell"})[7].text.encode("utf-8"))
            content_dict.update(
                {"Community_Name": community_info[:community_info.find(" ")]})
            content_dict.update(
                {"District": community_info[community_info.find("(") + 1:community_info.find(" ", community_info.find("("))]})
            content_dict.update(
                {"Area": community_info[community_info.find(" ", community_info.find("(")) + 2:community_info.find(")")]})
            content_dict.update({"Address":
                                     utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(
                                            name="span", attrs={
                                                "class": "item-cell"})[9].text.encode("utf-8"))})

            Seriel_Number = \
                utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(name="span", attrs={
                "class": "item-cell"})[13].text.encode("utf-8"))[:9]
            content_dict.update(
                {"Seriel_Number": Seriel_Number})
            House_Link = BASE_URL + "/ershoufang/" + Seriel_Number + ".html"
            content_dict.update(
                {"House_Link": House_Link})
            Community_Link = BASE_URL + utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(name="a", attrs={
                "class": "u-link"})[0].get("href"))
            content_dict.update(
                {"Community_Link": Community_Link})
            content_dict.update(
                {"Structure_Type": utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[1].find_all(name="span", attrs={
                    "class": "item-cell"})[1].text)})
            content_dict.update(
                {"Elevator": utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[1].find_all(name="span", attrs={
                    "class": "item-cell"})[3].text)})
            content_dict.update(
                {"Square_Meter": utilities.get_string_num(utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[1].find_all(name="span", attrs={
                    "class": "item-cell"})[5].text))})
            content_dict.update(
                {"Heating_Type": utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[1].find_all(name="span", attrs={
                    "class": "item-cell"})[7].text)})
            content_dict.update(
                {"Floor_Number": utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[2].find_all(name="span", attrs={
                    "class": "item-cell"})[1].text)})
            content_dict.update(
                {"Decoration_Level": utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[2].find_all(name="span", attrs={
                    "class": "item-cell"})[3].text)})
            content_dict.update(
                {"Orientation_Type": utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[2].find_all(name="span", attrs={
                    "class": "item-cell"})[5].text)})
            content_dict.update(
                {"Parking_Place": utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[2].find_all(name="span", attrs={
                    "class": "item-cell"})[7].text)})
            content_dict.update(
                {"Last_Trade_Date": utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[4].find_all(name="span", attrs={
                    "class": "item-cell"})[1].text)})
            content_dict.update(
                {"Restriction_Type": utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[4].find_all(name="span", attrs={
                    "class": "item-cell"})[3].text)})
            content_dict.update(
                {"Trade_Reason": utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[5].find_all(name="span", attrs={
                    "class": "item-cell"})[1].text)})
            content_dict.update(
                {"House_Type_Name": utilities.get_string_strip(bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[5].find_all(name="span", attrs={
                    "class": "item-cell"})[3].text)})
            content_dict.update(
                {"House_Type_Name": utilities.get_string_strip(
                    bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[5].find_all(name="span", attrs={
                        "class": "item-cell"})[3].text)})
            content_dict.update(
                {"House_Type_Name": utilities.get_string_strip(
                    bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[5].find_all(name="span", attrs={
                        "class": "item-cell"})[3].text)})

            content_dict.update({"Building_Num_on_Total":
                                     utilities.get_string_num(bsObj.find_all(name="div", attrs={"class": "module-col intro-col2"})[0].find_all(
                                         name="span")[7].text)})
            content_dict.update({"House_Num_on_Total":
                                     utilities.get_string_num(bsObj.find_all(name="div", attrs={"class": "module-col intro-col2"})[0].find_all(
                                         name="span")[9].text)})
            Sold_Rent_Num = utilities.get_string_strip(
                bsObj.find_all(name="div", attrs={"class": "module-col intro-col2"})[0].find_all(name="span")[15].text)
            content_dict.update({"House_Num_on_Sold": utilities.get_string_num(Sold_Rent_Num[:Sold_Rent_Num.find(" ")])})
            content_dict.update({"House_Num_on_Rent": utilities.get_string_num(Sold_Rent_Num[Sold_Rent_Num.find(" "):])})

            content_dict.update(
                {"Num_of_Visit_7": utilities.get_string_strip(bsObj.find_all(name="div", attrs={"id": "kanfangListVue"})[0].find_all(name="look-list")[
                    0].get("count7").encode("utf-8"))})
            content_dict.update(
                {"Num_of_Visit_90": utilities.get_string_strip(bsObj.find_all(name="div", attrs={"id": "kanfangListVue"})[0].find_all(name="look-list")[
                    0].get("count90").encode("utf-8"))})

            if len(bsObj.find_all(name="div", attrs={"id": "js-owner-comment"})) > 0:
                content_dict.update(
                    {"Owner_My_Story": utilities.get_string_strip(bsObj.find_all(name="div", attrs={"id": "js-owner-comment"})[0].find_all(name="li",
                                                                                                                 attrs={
                                                                                                                     "class": "comment-item"})[
                                           0].text.encode("utf-8"))[12:]})

                content_dict.update(
                    {"Owner_Decoration": utilities.get_string_strip(bsObj.find_all(name="div", attrs={"id": "js-owner-comment"})[0].find_all(name="li",
                                                                                                                   attrs={
                                                                                                                       "class": "comment-item"})[
                                             1].text.encode("utf-8")).replace('\n', '').replace(' ', '')[12:]})

                content_dict.update(
                    {"Owner_House_Feature": utilities.get_string_strip(bsObj.find_all(name="div", attrs={"id": "js-owner-comment"})[0].find_all(name="li",
                                                                                                                      attrs={
                                                                                                                          "class": "comment-item"})[
                                                2].text.encode("utf-8")).replace('\n', '').replace(' ', '')[12:]})

        elif content_type == "community":
            if bsObj.find_all(name="a", attrs={"class": "link_more"})<>[]:
                content_dict.update({"Gonglue_Link": utilities.get_string_strip(bsObj.find_all(name="a", attrs={"class": "link_more"})[0].get("href"))})

            content_dict.update(
                {"Everage_Price": utilities.get_string_strip(bsObj.find_all(name="span", attrs={"class": "p"})[0].text.encode("utf-8").replace(
                    '\n', ''))})
            content_dict.update(
                {"Community_Type": utilities.get_string_strip(bsObj.find_all(name="span", attrs={"class": "other"})[0].text.encode(
                    "utf-8").replace('\n', ''))})
            content_dict.update(
                {"Year_Build": utilities.get_string_num(utilities.get_string_strip(bsObj.find_all(name="span", attrs={"class": "other"})[1].text))})
            content_dict.update(
                {"PM_Fee": utilities.get_string_strip(bsObj.find_all(name="span", attrs={"class": "other"})[2].text.encode("utf-8"))})
            content_dict.update(
                {"PM_Company": utilities.get_string_strip(bsObj.find_all(name="span", attrs={"class": "other"})[3].text.encode("utf-8"))})
            #print(content_dict.get("PM_Company"))
            content_dict.update(
                {"Developer": utilities.get_string_strip(bsObj.find_all(name="span", attrs={"class": "other"})[4].text.encode("utf-8"))})
            content_dict.update({"Longitude": utilities.get_string_strip(bsObj.find_all(name="div", attrs={"id": "zoneMap"})[0].get("longitude"))})
            content_dict.update({"Latitude": utilities.get_string_strip(bsObj.find_all(name="div", attrs={"id": "zoneMap"})[0].get("latitude"))})
            content_dict.update(
                {"Seriel_Number": utilities.get_string_strip(bsObj.find_all(name="div", attrs={"id": "notice_focus"})[0].get("propertyno"))})

            content_dict.update(
                {"District_Link": BASE_URL +
                                  utilities.get_string_strip(bsObj.find_all(name="div", attrs={"class": "container"})[0].find_all(name="a")[2].get(
                                      "href"))})
            content_dict.update(
                {"Area_Link": BASE_URL + utilities.get_string_strip(bsObj.find_all(name="div", attrs={"class": "container"})[0].find_all(name="a")[
                    3].get("href"))})
            content_dict.update(
                {"Community_Link": BASE_URL +
                                   utilities.get_string_strip(bsObj.find_all(name="div", attrs={"class": "container"})[0].find_all(name="a")[
                                       4].get("href"))})
            content_dict.update(
                {"Community_Name": utilities.get_string_strip(bsObj.find_all(name="div", attrs={"class": "title fl"})[0].find_all(name="h1")[
                    0].text)})

            District_Area = utilities.get_string_strip(bsObj.find_all(name="div", attrs={"class": "title fl"})[0].find_all(name="span")[1].text)
            if District_Area.find(u"上海周边") > 0:
                District = District_Area[District_Area.find("(") + 1:District_Area.find("(") + 5]
                Area = District_Area[District_Area.find("(") + 5:District_Area.find(")")]
            else:
                District = District_Area[District_Area.find("(") + 1:District_Area.find("(") + 3]
                Area = District_Area[District_Area.find("(") + 3:District_Area.find(")")]

            content_dict.update({"District": District})
            content_dict.update({"Area": Area})
            content_dict.update(
                {"Address": utilities.get_string_strip(bsObj.find_all(name="div", attrs={"class": "title fl"})[0].find_all(name="span",
                                                                                                attrs={"class": "adr"})[
                    0].text)})

            House_on_Sold = utilities.get_string_strip(bsObj.find_all(name="div", attrs={"id": "res-nav"})[0].find_all(name="a", attrs={
                "gahref": "xiaoqu_nav_for_sale"})[0].text)

            content_dict.update(
                {"House_Num_on_Sold": House_on_Sold[House_on_Sold.find(u'（') + 1:House_on_Sold.find(u'）')]})

            content_dict.update(
                {"On_Sold_Link": BASE_URL + utilities.get_string_strip(bsObj.find_all(name="div", attrs={"id": "res-nav"})[0].find_all(name="a",
                                                                                                            attrs={
                                                                                                                "gahref": "xiaoqu_nav_for_sale"})[
                    0].get("href"))})

        return content_dict

    def html_parse_com_gonglue(self, content, content_dict):
        cur_code, cur_url, cur_html = content
        bsObj = BeautifulSoup(cur_html, "html.parser")

        count = len(bsObj.find_all(name="div", attrs={"class": "part js_content"}))
        i = 1
        for i in range(1, count+1):
            content_dict = self.html_parse_com_gonglue_reuse(bsObj, content_dict, i)

        return(content_dict)

    def html_parse_com_gonglue_reuse(self, bsObj, content_dict, seq):
        tag = "pgl_"+str(seq)
        count = len(bsObj.find_all(name="div", attrs={"id": tag })[0].find_all(name="p", attrs={"class", "q"}))
        trans_dict = {u"整体规划": "Compre_Plan",
                      u"小区概况": "Community_Overview",
                      u"位置环境": "Community_Env",
                      u"住户特征": "Household_Char",
                      u"周边配套": "Assist_Fac",
                      u"物业管理": "Estate_Manag",
                      u"楼栋特色": "Buiding_Char",
                      u"市场行情": "Market_Quo",
                      u"类似小区": "Sim_Community"
                      }
        title = utilities.get_string_strip(bsObj.find_all(name="div", attrs={"id": tag })[0].find_all(name="div", attrs={"class", "part-title"})[0].text)
        title = trans_dict.get(title)

        i = 0
        content = ""
        for i in range(0, count):
            content = utilities.get_string_strip(content + bsObj.find_all(name="div", attrs={"id": tag})[0].find_all(name="p", attrs={"class", "q"})[i].text) + "\n"
            content = content + utilities.get_string_strip(bsObj.find_all(name="div", attrs={"id": tag})[0].find_all(name="div", attrs={"class", "a"})[i].text) + "\n"
            i += 1
        content_dict.update({title:content})
        return(content_dict)

class LianjiaSaver(processor.Saver):
    def hash_fetch(self, hash_type):
        cur = self.conn.cursor()
        if hash_type == "house":
            cur.execute("SELECT Hash_Value FROM house_info_saf_2017")
        else:
            cur.execute("SELECT Hash_Value FROM community_info_saf_2017")
        orig_set = set(link[0] for link in cur)

        return (orig_set)

    def db_prep(self, type, content):
        if type == "house":
            content_list = [u'House_Title', u'House_Type_Name', u'Structure_Type', u'Decoration_Level'
                , u'Orientation_Type', u'Restriction_Type', u'Listing_Price', u'Square_Meter', u'Quoted_Price'
                , u'Floor_Number', u'Year_Build', u'District', u'Area', u'Address', u'Community_Name'
                , u'Ring_Line', u'Elevator', u'Heating_Type', u'Keys_Flag', u'Num_of_Visit_7', u'Num_of_Visit_90'
                , u'Last_Trade_Date', u'Owner_My_Story', u'Owner_Decoration', u'Owner_House_Feature', u'Seriel_Number'
                , u'House_Link', u'Hash_Value', u'Parking_Place', u'Trade_Reason']

            t = []
            #for keys, values in content.items(): print(keys + " : " + values)
            for column in content_list:
                if column in content:
                    t.append(content[column])
                else:
                    t.append(None)
        elif type == "community":
            content_list = [u'Community_Env',u'Assist_Fac',u'Estate_Manag',u'Community_Type',u'Community_Overview',
                        u'Compre_Plan',u'Sim_Community',u'Year_Build',u'Market_Quo',u'Everage_Price',u'Buiding_Char',u'PM_Company',
                        u'Household_Char',u'PM_Fee',u'Developer',u'Longitude',u'Latitude',u'Seriel_Number',u'District_Link',
                        u'Area_Link',u'Community_Link',u'Community_Name',u'House_Num_on_Sold',u'On_Sold_Link',u'Address',
                        u'District',u'Area', u'Hash_Value', u'House_Num_on_Rent', u'House_Num_on_Total', u'Building_Num_on_Total']

            t = []
            #for keys, values in content.items(): print(keys + " : " + values)
            for column in content_list:
                if column in content:
                    t.append(content[column])
                else:
                    t.append(None)
        t = tuple(t)
        #for i in t: print(i)
        return(t)

    def db_insert(self, type, dataset):
        cur = self.conn.cursor()
        if type == "house":
            cur.execute(
                "INSERT INTO house_info_saf_2017(House_Title, House_Type_Name, Structure_Type, Decoration_Level, Orientation_Type,"
                "Restriction_Type,Listing_Price, Square_Meter, Quoted_Price, Floor_Number, Year_Build, District,"
                "Area, Address, Community_Name, Ring_Line, Elevator, Heating_Type, Keys_Flag,"
                "Num_of_Visit_7, Num_of_Visit_90, Last_Trade_Date, "
                "Owner_My_Story, Owner_Decoration, Owner_House_Feature, Seriel_Number, House_Link, Hash_Value, Parking_Place, Trade_Reason) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (dataset))
        elif type == "community":
            cur.execute(
                "INSERT INTO community_info_saf_2017(Community_Env,Assist_Fac,Estate_Manag,Community_Type,Community_Overview,"
                "Compre_Plan,Sim_Community,Year_Build,Market_Quo,Everage_Price,Buiding_Char,PM_Company,"
                "Household_Char,PM_Fee,Developer,Longitude,Latitude,Seriel_Number,District_Link,"
                "Area_Link,Community_Link,Community_Name,House_Num_on_Sold,On_Sold_Link,Address,District,Area,Hash_Value"
                ",House_Num_on_Rent,House_Num_on_Total,Building_Num_on_Total) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (dataset))

        cur.connection.commit()

if __name__ == "__main__":
    """
    main process
    """
    fetcher = LianjiaFetcher(critical_max_repeat=3, critical_sleep_time=0)
    processor = LianjiaParser(max_deep=1, max_repeat=3)
    saver = LianjiaSaver(save_type="db", db_info=utilities.CONFIG_DB_INFO)

    global cur_house_hash_set
    global cur_community_hash_set

    cur_house_hash_set = saver.hash_fetch("house")
    cur_community_hash_set = saver.hash_fetch("community")

    House_Info_Type_Name="ershoufang"

    cur_code, content = fetcher.working(BASE_URL+"/"+House_Info_Type_Name, None, 1, 3)
    processor.html_parse(content, "main_links")
