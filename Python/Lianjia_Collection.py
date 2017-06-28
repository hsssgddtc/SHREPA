# -*- coding:utf-8 -*-

import urllib2

from __builtin__ import float
from bs4 import BeautifulSoup
import re
import pymysql
import time
import random

global BASE_URL
BASE_URL = 'http://sh.lianjia.com'
SOURCE = 'lianjia'

hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

conn = pymysql.connect(host='127.0.0.1', user='shai', passwd='Thermo20()', db='TEST', charset='utf8')
cur = conn.cursor()
cur.execute("USE SHREPA")


def main_url_gen(number, type):
    base_url = BASE_URL + '/' + type + '/d'
    # chengjiao: 1~2413 ; ershou: 1~1941
    main_url = base_url + str(number)
    return main_url


def getBSobj(url):
    try:
        #req = urllib2.Request(url, headers=hds[random.randint(0, len(hds) - 1)])
        req = urllib2.Request(url)
        html = urllib2.urlopen(req, timeout=10)
    except urllib2.HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html, "html.parser")
    except AttributeError as e:
        return None
    return bsObj

def getNextPage(url, content_type, house_link_set, community_link_set):
    try:
        bs_t = getBSobj(url)
        if bs_t.find(name="a",gahref="results_next_page") != []:
            next_url = BASE_URL + bs_t.find(name="a",gahref="results_next_page").get("href")
            getContent_Outside(next_url, content_type, house_link_set, community_link_set)
            getNextPage(next_url, content_type, house_link_set, community_link_set)
    except AttributeError as e:
        return None

def getContent_Outside(url, content_type, house_link_set, community_link_set):
    try:
        bs_t_1 = getBSobj(url)
        count = 1

        if content_type == "ershoufang":
            for content in bs_t_1.find_all(name="div", attrs={"class": "info-panel"}):
                print(count)
                if count % 11 == 0:
                    print("Positively Sleep for a while")
                    time.sleep(random.randint(5, 10))

                house_info_dict = {}    #refresh house dict
                community_info_dict = {}    #refresh community dict

                house_info_dict.update({"House_Source_Name": SOURCE})
                house_info_dict.update({"House_Info_Type_Name": content_type})
                community_info_dict.update({"Community_Source_Name": SOURCE})

                if BASE_URL + content.find_all(name="a")[0].get("href") not in house_link_set:
                    detail_info_list = content.div.find_all(name="span", attrs={"class": None},
                                                         text=lambda x: x != "|")
                    house_info_dict.update({"Metro":"N/A"})
                    house_info_dict.update({"Restriction_Type": "N/A"})
                    house_info_dict.update({"Keys_Flag": "N/A"})
                    if (len(detail_info_list) == 4):
                        if (len(detail_info_list[2].get_text()) < 5):
                            house_info_dict.update({"Restriction_Type": detail_info_list[2].get_text()})
                            house_info_dict.update({"Keys_Flag": detail_info_list[3].get_text()})
                        else:
                            house_info_dict.update({"Metro": detail_info_list[2].get_text()})
                            if (len(detail_info_list[3].get_text()) == 2):
                                house_info_dict.update({"Restriction_Type": detail_info_list[3].get_text()})
                            else:
                                house_info_dict.update({"Keys_Flag": detail_info_list[3].get_text()})
                    elif (len(detail_info_list) == 5):
                        house_info_dict.update({"Metro": detail_info_list[2].get_text()})
                        house_info_dict.update({"Restriction_Type": detail_info_list[3].get_text()})
                        house_info_dict.update({"Keys_Flag": detail_info_list[4].get_text()})
                    elif (len(detail_info_list) == 3):
                        if (len(detail_info_list[2].get_text()) < 5):
                            if (len(detail_info_list[2].get_text()) == 2):
                                house_info_dict.update({"Restriction_Type": detail_info_list[2].get_text()})
                            else:
                                house_info_dict.update({"Keys_Flag": detail_info_list[2].get_text()})
                        else:
                            house_info_dict.update({"Metro": detail_info_list[2].get_text()})

                    num_info_list = content.find_all(name="span", attrs={"class": "num"})

                    house_info_dict.update({"Listing_Price": num_info_list[0].get_text().encode("utf-8") + "万"})
                    house_info_dict.update({"Num_of_Visit": num_info_list[1].get_text().encode("utf-8") + "人"})

                    house_info_dict.update({"House_Title": content.find_all(name="a")[0].get("title")})
                    house_info_dict.update({"Square_Meter": detail_info_list[1].get_text()})
                    house_info_dict.update({"District": content.find_all(name="a")[2].get_text()})
                    house_info_dict.update({"Area": content.find_all(name="a")[3].get_text()})
                    house_info_dict.update({"Community_Name": content.find_all(name="a")[1].get_text()})
                    house_info_dict.update({"House_Link": BASE_URL + content.find_all(name="a")[0].get("href")})
                    house_info_dict.update({"Community_Link": BASE_URL + content.find_all(name="a")[1].get("href")})
                    house_info_dict.update({"District_Link": BASE_URL + content.find_all(name="a")[2].get("href")})
                    house_info_dict.update({"Area_Link": BASE_URL + content.find_all(name="a")[3].get("href")})

                    community_info_dict.update({"Community_Name": content.find_all(name="a")[1].get_text()})
                    community_info_dict.update({"District": content.find_all(name="a")[2].get_text()})
                    community_info_dict.update({"Area": content.find_all(name="a")[3].get_text()})
                    community_info_dict.update({"Community_Link": BASE_URL + content.find_all(name="a")[1].get("href")})
                    community_info_dict.update({"District_Link": BASE_URL + content.find_all(name="a")[2].get("href")})
                    community_info_dict.update({"Area_Link": BASE_URL + content.find_all(name="a")[3].get("href")})

                    getContent_Inside_House(house_info_dict["House_Link"], content_type, house_info_dict)
                    count += 1
                    if house_info_dict["Community_Link"] not in community_link_set:
                        getContent_Inside_Community(house_info_dict["Community_Link"], community_info_dict)
                    print("*********************************")

                else:
                    print("link exists!!!!!")
            else:
                #this is for chengjiao
                for content in bs_t_1.find_all(name="div", attrs={"class": "info-panel clear"}):
                    house_info_dict.update({"House_Link": BASE_URL + content.find_all(name="a")[0].get("href")})

                    # Court_Link.append(BASE_URL + link.find_all(name="a")[1].get("href"))
                    title_tmp = content.find_all(name="a")[0].get_text()
                    house_info_dict.update({"Structure_Type": title_tmp[title_tmp.index(" ") + 1:title_tmp.index(" ",
                                                                                                                 title_tmp.index(
                                                                                                                     " ") + 1)]})
                    house_info_dict.update({"Square_Meter": title_tmp[title_tmp.index(" ", title_tmp.index(" ") + 1) + 1:]})
                    house_info_dict.update({"District": content.find_all(name="a")[1].get_text()})
                    house_info_dict.update({"District_Link": BASE_URL + content.find_all(name="a")[1].get("href")})
                    house_info_dict.update({"Area": content.find_all(name="a")[2].get_text()})
                    house_info_dict.update({"Area_Link": BASE_URL + content.find_all(name="a")[2].get("href")})

                    house_info_dict.update({"Metro":"N/A"})
                    house_info_dict.update({"Restriction_Type": "N/A"})
                    house_info_dict.update({"Keys_Flag": "N/A"})
                    if content.find(name="div", attrs={"class": "introduce"}) is not None:
                        rest_me_list = content.find(name="div", attrs={"class": "introduce"}).find_all(name="span")
                        if (len(rest_me_list) == 1):
                            if (len(rest_me_list[0].string) < 5):
                                house_info_dict.update({"Restriction_Type": rest_me_list[0].get_text()})
                            else:
                                house_info_dict.update({"Metro": rest_me_list[0].get_text()})
                        else:
                            house_info_dict.update({"Metro": rest_me_list[0].get_text()})
                            house_info_dict.update({"Restriction_Type": rest_me_list[1].get_text()})
                    house_info_dict = getContent_Inside_House(house_info_dict["House_Link"], content_type, house_info_dict)
                    #if house_info_dict["Community_Link"] not in community_link_set:
                    #    getContent_Inside_Community(house_info_dict["Community_Link"], community_info_dict)
                    print("*********************************")
    except AttributeError as e:
        return None

def getContent_Inside_House(url, content_type, house_info_dict):
    bs_t_1 = getBSobj(url)
    content_list = []
    final_list = []

    if content_type == "ershoufang":
        content_list.append(bs_t_1.find_all(name="td")[0].get_text())
        content_list.append(bs_t_1.find_all(name="td")[1].get_text())
        content_list.append(bs_t_1.find_all(name="td")[2].get_text())
        content_list.append(bs_t_1.find_all(name="td")[3].get_text())
        content_list.append(bs_t_1.find_all(name="td")[4].get_text())
        content_list.append(bs_t_1.find_all(name="td")[5].get_text())
        content_list.append(bs_t_1.find_all(name="td")[6].get_text())
        content_list.append(bs_t_1.find_all(name="td")[8].get_text())
        content_list.append(bs_t_1.find_all(name="td")[9].get_text())
    
        for content in bs_t_1.find_all("li"):
            # print(content.get_text().encode("utf-8"))
            if (re.match("房屋户型", content.get_text().encode("utf-8"))):
                content_list.append(content.get_text())
            elif (re.match("梯户比例", content.get_text().encode("utf-8"))):
                content_list.append(content.get_text())
            elif (re.match("上次交易", content.get_text().encode("utf-8"))):
                content_list.append(content.get_text())
            elif (re.match("房屋类型", content.get_text().encode("utf-8"))):
                content_list.append(content.get_text())
    
        for content in content_list:
            rep_content = content.replace("\r", "").replace("\n", "").replace(" ", "").replace("	", "").encode(
                "utf-8")
    
            if rep_content.find("：") > 0:
                ind = rep_content.index("：") + 3
            else:
                ind = 0
            final_list.append(rep_content[ind:])

        house_info_dict.update({"Quoted_Price":final_list[0]})
        house_info_dict.update({"Floor_Number": final_list[1]})
        house_info_dict.update({"Year_Build": final_list[2]})
        house_info_dict.update({"Decoration_Level": final_list[3]})
        house_info_dict.update({"Orientation_Type": final_list[4]})
        house_info_dict.update({"Down_Payment": final_list[5]})
        house_info_dict.update({"Mortgage_Payment": final_list[6]})
        house_info_dict.update({"Address": final_list[7]})
        house_info_dict.update({"Seriel_Number": final_list[8]})
        house_info_dict.update({"Structure_Type": final_list[9]})
        house_info_dict.update({"House_Proportion": final_list[10]})
        house_info_dict.update({"Last_Trade_Date": final_list[11]})
        house_info_dict.update({"House_Type_Name": final_list[12]})
        house_info_dict.update({"Longitude": bs_t_1.find(name="div", id="zoneMap").get("longitude")})
        house_info_dict.update({"Latitude": bs_t_1.find(name="div", id="zoneMap").get("latitude")})
    
        #for each in house_info_dict:
        #    print(each + ":" + house_info_dict[each])
    else:
        final_list.append(bs_t_1.find_all(name="p")[:2])
        for content in bs_t_1.find_all(name="td"):
            rep_content = content.text.replace("\r", "").replace("\n", "").replace(" ", "").replace("	", "").encode(
                "utf-8")
            if rep_content.find("：") > 0:
                ind = rep_content.index("：") + 3
            else:
                ind = 0
            if content.a is not None:
                final_list.append(BASE_URL + content.a.get("href").encode("utf-8"))
            final_list.append(rep_content[ind:])

    #for item in final_list:
    #    print(item)
    #exit(0)
    insert_house_data(house_info_dict)
    #return(house_info_dict)

def getContent_Inside_Community(url, community_info_dict):
    bs_t_1 = getBSobj(url)
    content_list = []

    for content in bs_t_1.find_all(name="div", attrs={"class": "res-info fr"}):
        for content_detail in content.find_all(name="span", attrs={"class": "other"}):
            content_list.append(content_detail.get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace("	","").encode("utf-8"))

        if content.find_all(name="span", attrs={"class": "p"}) <> []:
            content_list.append(content.find_all(name="span", attrs={"class": "p"})[0].get_text().replace("\r", "").replace("\n","").replace(" ", "").replace("	", "").encode("utf-8"))
        else:
            content_list.append("暂无挂牌均价")

    house_on_sold = bs_t_1.find_all(name="a", attrs={"gahref": "xiaoqu_nav_for_sale"})[
                       0].get_text().encode(
                       "utf-8")
    if house_on_sold.find("（") > 0:
        content_list.append(house_on_sold[house_on_sold.index("（") + 3:house_on_sold.index("）")])
    else:
        content_list.append(0)

    community_info_dict.update({"Community_Type": content_list[0]})
    community_info_dict.update({"Year_Build": content_list[1]})
    community_info_dict.update({"PM_Fee": content_list[2]})
    community_info_dict.update({"PM_Company": content_list[3]})
    community_info_dict.update({"Developer": content_list[4]})
    community_info_dict.update({"Building_Num_on_Total": content_list[5]})
    community_info_dict.update({"House_Num_on_Total": content_list[6]})
    community_info_dict.update({"Quoted_Price": content_list[7]})
    community_info_dict.update({"House_Num_on_Sold": content_list[8]})
    community_info_dict.update({"Address": bs_t_1.find(name="span", attrs={"class":"adr"}).get_text()})
    community_info_dict.update({"Longitude": bs_t_1.find(name="div", id="zoneMap").get("longitude")})
    community_info_dict.update({"Latitude": bs_t_1.find(name="div", id="zoneMap").get("latitude")})
    community_info_dict.update({"On_Sold_Link": BASE_URL + bs_t_1.find(name="a", gahref="for_sale_view_all").get("href")})

    #for each in community_info_dict:
    #    print(each + ":" + community_info_dict[each])
    #exit(0)
    insert_community_data(community_info_dict)


def get_links(link_type):
    if link_type == "house":
        cur.execute("SELECT House_Link FROM house_info_saf_new")
    else:
        cur.execute("SELECT Community_Link FROM community_info_saf_new")
    orig_set = set(link[0] for link in cur)
    return (orig_set)

def insert_house_data(house_info_dict):
    house_info_list=[u'House_Source_Name',u'House_Info_Type_Name',u'House_Type_Name',u'Structure_Type',u'Decoration_Level'
        ,u'Orientation_Type',u'Restriction_Type',u'House_Title',u'Listing_Price',u'Square_Meter',u'Quoted_Price'
        ,u'Down_Payment',u'Mortgage_Payment',u'Floor_Number',u'House_Proportion',u'Year_Build',u'District',u'Area'
        ,u'Address',u'Longitude',u'Latitude',u'Community_Name',u'Metro',u'Keys_Flag',u'Num_of_Visit',u'Last_Trade_Date'
        ,u'Additional_Content',u'Seriel_Number',u'House_Link',u'Community_Link',u'District_Link',u'Area_Link']

    t=[]
    for column in house_info_list:
        if column in house_info_dict:
            t.append(house_info_dict[column])
        else:
            t.append(None)

    t=tuple(t)

    cur.execute("INSERT INTO house_info_saf_new(House_Source_Name,House_Info_Type_Name,House_Type_Name,Structure_Type"
                ",Decoration_Level,Orientation_Type,Restriction_Type,House_Title,Listing_Price,Square_Meter"
                ",Quoted_Price,Down_Payment,Mortgage_Payment,Floor_Number,House_Proportion,Year_Build,District"
                ",Area,Address,Longitude,Latitude,Community_Name,Metro,Keys_Flag,Num_of_Visit,Last_Trade_Date"
                ",Additional_Content,Seriel_Number,House_Link,Community_Link,District_Link,Area_Link) \
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                (t))

    cur.connection.commit()
    print("insert house data done")

def insert_community_data(community_info_dict):
    community_info_list=[u'Community_Name',u'Community_Source_Name',u'Community_Type',u'Total_Square_Meter',u'Quoted_Price'
        ,u'Chain_Increase',u'Year_Build',u'District',u'Area',u'Address',u'Longitude',u'Latitude',u'House_Num_on_Sold'
        ,u'House_Num_on_Rent',u'Building_Num_on_Total',u'House_Num_on_Total',u'PM_Fee',u'PM_Company',u'Developer'
        ,u'Plot_Ratio',u'Letting_Ratio',u'Parking_Lot',u'Greening_Ratio',u'Metro',u'Kingdergarten',u'Elementary_School'
        ,u'Middle_School',u'High_School',u'Label',u'Additional_Content',u'Seriel_Number',u'Community_Link'
        ,u'District_Link',u'Area_Link',u'On_Sold_Link']

    t=[]
    for column in community_info_list:
        if column in community_info_dict:
            t.append(community_info_dict[column])
        else:
            t.append(None)

    t=tuple(t)

    cur.execute("INSERT INTO community_info_saf_new(Community_Name,Community_Source_Name,Community_Type"
                ",Total_Square_Meter,Quoted_Price,Chain_Increase,Year_Build,District,Area,Address"
                ",Longitude,Latitude,House_Num_on_Sold,House_Num_on_Rent,Building_Num_on_Total"
                ",House_Num_on_Total,PM_Fee,PM_Company,Developer,Plot_Ratio,Letting_Ratio"
                ",Parking_Lot,Greening_Ratio,Metro,Kingdergarten,Elementary_School,Middle_School"
                ",High_School,Label,Additional_Content,Seriel_Number,Community_Link,District_Link"
                ",Area_Link,On_Sold_Link) \
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                (t))

    cur.connection.commit()
    print("insert community data done")


def GetCurrentTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))


if __name__ == '__main__':
    house_link_set = get_links("house")
    community_link_set = get_links("community")

    try:
        for House_Info_Type_Name in ("ershoufang","chengjiao"):
            bs_t_1 = getBSobj(BASE_URL + '/' + House_Info_Type_Name)

            for content in bs_t_1.find_all(name="div", attrs={"class": "option-list gio_district"}):
                for item in content.find_all(name="a", gahref=re.compile("^((?!(district-nolimit|pudong|jiading|fengxian|baoshan|chongming|)).)*$")):
                    DISTRICT_URL = BASE_URL + item.get("href")
                    print("Current District: " + item.get_text())
                    bs_t_2 = getBSobj(DISTRICT_URL)

                    for sub_content in bs_t_2.find_all(name="div",
                                                       attrs={"class": "option-list sub-option-list gio_plate"}):
                        for sub_item in sub_content.find_all(name="a", gahref=re.compile("^((?!(plate-nolimit|chunshen|gumei)).)*$")):
                            AREA_URL = BASE_URL + sub_item.get("href")
                            print("Current Area: " + sub_item.get_text())

                            getContent_Outside(AREA_URL, House_Info_Type_Name, house_link_set, community_link_set)
                            getNextPage(AREA_URL, House_Info_Type_Name, house_link_set, community_link_set)
                    print("***************************************")

    except Exception  as exp_msg:
        print(exp_msg)
    finally:
        print(GetCurrentTime())
        print("Done!!!!!!")
