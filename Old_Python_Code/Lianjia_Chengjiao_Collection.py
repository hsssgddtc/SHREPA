# -*- coding:utf-8 -*-

import urllib2
import BeautifulSoup
import re
import pymysql
import time
import random

BASE_URL = 'http://sh.lianjia.com'
SOURCE = 'lianjia'
DISTRICT_CN = ['浦东', '闵行', '宝山', '徐汇', '普陀', '杨浦', '长宁', '松江', '嘉定', '黄浦', '静安', '闸北', '虹口', '青浦', '奉贤', '金山', '崇明',
               '上海周边']

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Thermo2014!', db='SHREPA', charset='utf8')
cur = conn.cursor()
cur.execute("USE SHREPA")

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


def getSubstring_colon(orig_str):
    if orig_str.find("：") > 0:
        ind = orig_str.index("：") + 3
    else:
        ind = 0
    return(orig_str[ind:])

def getSubstring_line(orig_str, segment):
    if orig_str.find("-") > 0:
        if segment == 1:
            return(orig_str[:orig_str.index("-")])
        elif segment == 2:
            return(orig_str[orig_str.index("-")+1:orig_str.index("-",orig_str.index("-")+1)])
        else:
            return(orig_str[orig_str.index("-", orig_str.index("-") + 1)+1:])
    else:
        return None

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

def get_links(link_type):
    if link_type == "house":
        cur.execute("SELECT House_Link FROM house_info_saf_new_chengjiao")
    else:
        cur.execute("SELECT Community_Link FROM community_info_saf_new_chengjiao")
    orig_set = set(link[0] for link in cur)
    return (orig_set)

def getExistingInfo(community_url, community_info_dict):
    print(community_url)
    cur.execute("SELECT CASE WHEN Community_Type is not NULL THEN Community_Type ELSE 'N/A' END AS Community_Type \
                , CASE WHEN Longitude is not NULL THEN Longitude ELSE 'N/A' END AS Longitude \
                , CASE WHEN Latitude is not NULL THEN Latitude ELSE 'N/A' END AS Latitude FROM community_info_saf_new_chengjiao"
                " WHERE Community_Link = '" + community_url + "'")

    data_list = list(cur.fetchone())

    community_info_dict.update({"Community_Type": data_list[0]})
    community_info_dict.update({"Longitude": data_list[1]})
    community_info_dict.update({"Latitude": data_list[2]})

    return (community_info_dict)

def getContent_Inside_House(bs_t_1, house_info_dict):
    try:
        house_info_dict.update({"House_Source_Name": SOURCE})
        house_info_dict.update({"House_Info_Type_Name": "chengjiao"})

        tmp_title = bs_t_1.find(name="h1").get_text()
        print(tmp_title)

        house_info_dict.update({"House_Title": tmp_title})
        house_info_dict.update(
            {"Structure_Type": tmp_title[tmp_title.index(" "):tmp_title.index(" ", tmp_title.index(" ") + 1)]})
        house_info_dict.update({"Square_Meter": tmp_title[tmp_title.index(" ", tmp_title.index(" ") + 1) + 1:]})

        house_info_dict.update({"Last_Trade_Date": bs_t_1.find_all(name="p")[0].get_text()})
        house_info_dict.update({"Listing_Price": bs_t_1.find_all(name="p")[1].get_text()})



        house_info_dict.update({"Metro": (
        lambda x: x.find(name="span", attrs={"class": "fang-subway-ex"}).get_text() if x.find(name="span", attrs={
            "class": "fang-subway-ex"}) is not None else "N/A")(bs_t_1)})
        house_info_dict.update({"Restriction_Type": (
        lambda x: x.find(name="span", attrs={"class": "taxfree-ex"}).get_text() if x.find(name="span", attrs={
            "class": "taxfree-ex"}) is not None else "N/A")(bs_t_1)})

        house_info_dict.update({"Quoted_Price": getSubstring_colon(
            bs_t_1.find_all(name="td")[0].get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace(
                "	", "").encode("utf-8"))})
        house_info_dict.update({"Floor_Number": getSubstring_colon(
            bs_t_1.find_all(name="td")[1].get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace(
                "	", "").encode("utf-8"))})
        house_info_dict.update({"Year_Build": getSubstring_colon(
            bs_t_1.find_all(name="td")[2].get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace(
                "	", "").encode("utf-8"))})
        house_info_dict.update({"Decoration_Level": getSubstring_colon(
            bs_t_1.find_all(name="td")[3].get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace(
                "	", "").encode("utf-8"))})
        house_info_dict.update({"Orientation_Type": getSubstring_colon(
            bs_t_1.find_all(name="td")[4].get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace(
                "	", "").encode("utf-8"))})
        house_info_dict.update({"Community_Name": getSubstring_colon(
            bs_t_1.find_all(name="td")[5].get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace(
                "	", "").encode("utf-8"))})

        [(m.start(0), m.end(0)) for m in re.finditer('|'.join(DISTRICT_CN), house_info_dict["Community_Name"])]
        if re.match('|'.join(DISTRICT_CN), house_info_dict["Community_Name"]) is not None:
            house_info_dict.update({"District": house_info_dict["Community_Name"][m.start(0):m.end(0)]})
            house_info_dict.update({"Area": house_info_dict["Community_Name"][m.end(0):len(house_info_dict["Community_Name"]) - 3]})
            house_info_dict.update({"Community_Name": house_info_dict["Community_Name"][:m.start(0) - 3]})
        else:
            house_info_dict.update({"District": "N/A"})
            house_info_dict.update({"Area": "N/A"})

        house_info_dict.update({"Address": getSubstring_colon(
            bs_t_1.find_all(name="td")[6].get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace(
                "	", "").encode("utf-8"))})
        house_info_dict.update({"Seriel_Number": getSubstring_colon(
            bs_t_1.find_all(name="td")[7].get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace(
                "	", "").encode("utf-8"))})
        house_info_dict.update({"Additional_Content": getSubstring_colon(
            bs_t_1.find_all(name="td")[8].get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace(
                "	", "").encode("utf-8"))})

        house_info_dict.update({"Community_Link": BASE_URL + bs_t_1.find_all(name="td")[5].a.get("href")})
        house_info_dict.update({"On_Sold_Link": BASE_URL + bs_t_1.find_all(name="td")[8].a.get("href")})
    except AttributeError as e:
        return None

    return(house_info_dict)

def getContent_Inside_Community(url, community_info_dict):
    bs_t_1 = getBSobj(url)
    content_list = []

    #print(bs_t_1)
    for content in bs_t_1.find_all(name="div", attrs={"class": "res-info fr"}):
        for content_detail in content.find_all(name="span", attrs={"class": "other"}):
            content_list.append(content_detail.get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace("	","").encode("utf-8"))

        if content.find_all(name="span", attrs={"class": "p"}) <> []:
            content_list.append(content.find_all(name="span", attrs={"class": "p"})[0].get_text().replace("\r", "").replace("\n","").replace(" ", "").replace("	", "").encode("utf-8"))
        else:
            content_list.append("暂无挂牌均价")

    if bs_t_1.find_all(name="a", attrs={"gahref": "xiaoqu_nav_for_sale"}) == []\
            or bs_t_1.find_all(name="a", attrs={"gahref": "xiaoqu_nav_for_sale"})[
                           0].get_text().encode(
                           "utf-8").find("（") < 0:
        content_list.append(0)
    else:
        house_on_sold = bs_t_1.find_all(name="a", attrs={"gahref": "xiaoqu_nav_for_sale"})[
                           0].get_text().encode(
                           "utf-8")
        content_list.append(house_on_sold[house_on_sold.index("（") + 3:house_on_sold.index("）")])

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
    community_info_dict.update({"On_Sold_Link": (lambda x : BASE_URL + x.get("href") if x is not None else None)(bs_t_1.find(name="a", gahref="for_sale_view_all"))})

    #for each in community_info_dict:
    #    print(each + ":" + community_info_dict[each])
    #exit(0)
    return(community_info_dict)

def insert_house_data(house_info_dict):
    house_info_list=[u'House_Source_Name',u'House_Info_Type_Name',u'House_Type',u'Structure_Type',u'Decoration_Level'
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

    cur.execute("INSERT INTO house_info_saf_new_chengjiao(House_Source_Name,House_Info_Type_Name,House_Type,Structure_Type"
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

    cur.execute("INSERT INTO community_info_saf_new_chengjiao(Community_Name,Community_Source_Name,Community_Type"
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
        for num in xrange(4211309, 4211310):
            #1000001~1062609
            #4200000~?


            #if num % 40 == 0:
            #    print("Positively Sleep for a while")
            #    time.sleep(random.randint(15, 20))

            url = BASE_URL + '/chengjiao/sh' + str(num) + '.html'
            house_info_dict = {}
            community_info_dict = {}
            print("*******************************************")
            print(url)
            bs_t_1 = getBSobj(url)

            print(re.match('浦东',getSubstring_colon(
            bs_t_1.find_all(name="td")[5].get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace(
                "	", "").encode("utf-8"))))
            exit(0)

            if bs_t_1 is None or bs_t_1.find("h1").get_text() == '404':
                pass
            elif bs_t_1.find(name="div",attrs={"class":"errorPage"}) is not None:
                print("IP block, Positively Sleep for a while")
                time.sleep(50)
            else:

                if url not in house_link_set and re.match('|'.join(DISTRICT_CN), getSubstring_colon(
            bs_t_1.find_all(name="td")[5].get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace(
                "	", "").encode("utf-8"))) is not None:
                    house_info_dict.update({"House_Link": url})
                    house_info_dict.update({"House_Source_Name": SOURCE})

                    house_info_dict = getContent_Inside_House(bs_t_1, house_info_dict)

                    if house_info_dict["Community_Link"] not in community_link_set:
                        community_info_dict.update({"Community_Source_Name": SOURCE})
                        community_info_dict.update({"Community_Link": house_info_dict["Community_Link"]})
                        community_info_dict.update({"Community_Name": house_info_dict["Community_Name"]})

                        community_info_dict.update({"District": house_info_dict["District"]})
                        community_info_dict.update({"Area": house_info_dict["Area"]})

                        if house_info_dict["Metro"] is not None:
                            community_info_dict.update({"Metro": house_info_dict["Metro"]})

                        community_info_dict = getContent_Inside_Community(house_info_dict["Community_Link"],
                                                                          community_info_dict)

                    else:
                        community_info_dict = getExistingInfo(house_info_dict["Community_Link"], community_info_dict)
                        print("community link exists")

                    if community_info_dict["Community_Type"] is not None:
                        house_info_dict.update({"House_Type": community_info_dict["Community_Type"]})
                    if community_info_dict["Longitude"] is not None:
                        house_info_dict.update({"Longitude": community_info_dict["Longitude"]})
                    if community_info_dict["Latitude"] is not None:
                        house_info_dict.update({"Latitude": community_info_dict["Latitude"]})
                else:
                    print("house link exists")



                if url not in house_link_set and re.match('|'.join(DISTRICT_CN), getSubstring_colon(
            bs_t_1.find_all(name="td")[5].get_text().replace("\r", "").replace("\n", "").replace(" ", "").replace(
                "	", "").encode("utf-8"))) is not None:
                    insert_house_data(house_info_dict)

                    if house_info_dict["Community_Link"] not in community_link_set:
                        insert_community_data(community_info_dict)

    except Exception  as exp_msg:
        print(exp_msg)
    finally:
        print(GetCurrentTime())
        print("Done!!!!!!")
