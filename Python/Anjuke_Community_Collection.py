# -*- coding: utf-8 -*-
"""
@author: Sky
"""

import urllib2
from bs4 import BeautifulSoup
import re
import pymysql
import time
import random
import sys
#import lxml

reload(sys)
sys.setdefaultencoding("utf-8")

global BASE_URL
BASE_URL = "http://shanghai.anjuke.com"

conn = pymysql.connect(host='127.0.0.1', user='shai', passwd='Thermo20()', db='TEST', charset='utf8')
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

def main_url_gen(number, type):
    return(BASE_URL + '/' + type + '/p' + str(number))


def getBSobj(url):

    try:
        req = urllib2.Request(url, headers=hds[random.randint(0, len(hds) - 1)])
        html = urllib2.urlopen(req, timeout=10)
    except urllib2.HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html, "html.parser")
    except AttributeError as e:
        return None
    return bsObj

def get_links():
    cur.execute("SELECT Community_Link FROM community_info_saf")
    orig_set = set(link[0] for link in cur)
    return (orig_set)

def store_date(info_dict):
    info_list=[u'Community_Name',u'House_Type',u'Total_Square_Meter',u'Quoted_Price',u'Chain_Increase',u'Year_Build'
        ,u'District',u'Area',u'Address',u'House_Num_on_Sold',u'House_Num_on_Rent',u'Building_Num_on_Total',u'House_Num_on_Total'
        ,u'PM_Fee', u'PM_Company', u'Developer', u'Plot_Ratio', u'Letting_Ratio', u'Parking_Lot', u'Greening_Ratio'
        ,u'Metro', u'Label',  u'Additional_Content', u'Seriel_Number', u'Community_Link', u'District_Link'
        ,u'Area_Link', u'On_Sold_Link']

    t=[]
    for column in info_list:
        if column in info_dict:
            t.append(info_dict[column])
        else:
            t.append(None)

    t=tuple(t)

    cur.execute("INSERT INTO community_info_saf(Community_Name, House_Type, Total_Square_Meter, Quoted_Price, Chain_Increase, Year_Build, \
    District, Area, Address, House_Num_on_Sold, House_Num_on_Rent, Building_Num_on_Total, House_Num_on_Total, PM_Fee, PM_Company, \
    Developer, Plot_Ratio, Letting_Ratio, Parking_Lot, Greening_Ratio, Metro, Label, Additional_Content, Seriel_Number,\
     Community_Link, District_Link, Area_Link, On_Sold_Link ) \
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                (t))

    cur.connection.commit()
    print("insert data done")

def GetCurrentTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

if __name__ == '__main__':
    link_set = get_links()
    cnt = 1
    init_url = "http://shanghai.anjuke.com/community/"
    DISTRICT = ['pudong', 'minhang', 'xuhui', 'putuo', 'changning', 'jingan', 'huangpu', 'luwan', 'hongkou', 'zhabei',
                'yangpu', 'baoshan', 'songjiang', 'jiading', 'qingpu', 'fengxian', 'jinshan', 'chongming',
                'shanghaizhoubian']
    url_set = set()
    url_per_set = set()

    try:
        bs_t_1 = getBSobj(init_url)

        #for content in bs_t_1.find_all(name="div", attrs={"class": "div-border items-list"}):
        #    for item in content.find_all(href=re.compile("|".join(DISTRICT))):
        #        """Get the url of each district"""
        #        district_url = item.get("href")
        #        print("Current_District:" + item.get_text())
        #        bs_t_2 = getBSobj(item.get("href"))
#
        #        for sub_content in bs_t_2.find_all(name="div", attrs={"class": "sub-items"}):
        #            for sub_item in sub_content.find_all(name="a", href=lambda x: x != district_url):
        #                """Get the url of each area"""
        #                area_url = sub_item.get("href")
        #                if area_url not in url_set:
        #                    url_set.add(area_url)
        #                    print("Current_Area:" + sub_item.get_text().replace("\r", "")
        #                          .replace("\n", "").replace(" ", "").replace("	", "").encode("utf-8"))
        #                    bs_t_3 = getBSobj(area_url)
#
        #                    for inter_sub_content in bs_t_3.find_all(name="div", attrs={"class": "multi-page"}):
        #                        for inter_sub_item in inter_sub_content.find_all(name="a"):
        #                            """Get the url of each area_community"""
        #                            comm_url = inter_sub_item.get("href")
        #                            if comm_url not in url_set:
        #                                url_set.add(comm_url)
#
        print("*************************************")

        for each in ['http://shanghai.anjuke.com/community/view/657210/']:
            print("Current_URL:" + each)
            bs_t_1 = getBSobj(each)

            if bs_t_1.find_all(name="div", attrs={"_soj": "xqlb"}) <> []:
                for content in bs_t_1.find_all(name="div", attrs={"_soj": "xqlb"}):
                    info_dict = {}
                    ind_url = BASE_URL + content.find(name="a", attrs={"title": True}).get("href")
                    # print(ind_url)
                    #if cnt % 80 == 0:
                    #    time.sleep(60)
                    if ind_url not in link_set and ind_url not in ("http://shanghai.anjuke.com/community/view/5372/","http://shanghai.anjuke.com/community/view/658803/"):
                        info_dict.update({u'Community_Name': content.find(name="a",
                                                                          attrs={"title": True}).get(
                            "title")})
                        info_dict.update({u'Quoted_Price': content.find(
                            name="strong").get_text().replace("\r", "").replace("\n", "")})
                        info_dict.update({u'Chain_Increase': content.find(name="p", attrs={
                            "class": "price-txt"}).get_text().replace("\r", "")
                                         .replace("\n", "").replace("↑", "+").replace("↓", "-")})
                        info_dict.update({u'Community_Link': ind_url})
                        # print("*********************")
                        sleep_period = random.randint(2, 7)
                        print("randomly sleep for " + str(sleep_period) + " seconds")
                        time.sleep(sleep_period)

                        bs_t_2 = getBSobj(ind_url)
                        ind = 0

                        if bs_t_2.find_all(name="div", attrs={"class": "border-info comm-detail"}) <> []:
                            for content_detail in bs_t_2.find_all(name="div", attrs={
                                "class": "border-info comm-detail"}):

                                if content_detail.find_all(name="dd") <> []:
                                    for content_detail_item in content_detail.find_all(name="dd"):
                                        content_detail_item_info = content_detail_item.get_text().replace("\r",
                                                                                                          "").replace(
                                            "\n", "").replace("                        ",
                                                              " ").lstrip()
                                        # print(content_detail_item_info)
                                        if ind == 1:
                                            if content_detail_item_info.find(" ") > 0:
                                                info_dict.update({u'District': content_detail_item_info[
                                                                               :content_detail_item_info.index(
                                                                                   " ")]})
                                                info_dict.update({u'Area': content_detail_item_info[
                                                                           content_detail_item_info.index(
                                                                               " ") + 1:]})
                                            else:
                                                info_dict.update({u'District': content_detail_item_info})
                                        elif ind == 2:
                                            info_dict.update({u'Address': content_detail_item_info})
                                        elif ind == 3:
                                            info_dict.update({u'Developer': content_detail_item_info})
                                        elif ind == 4:
                                            info_dict.update({u'PM_Company': content_detail_item_info})
                                        elif ind == 5:
                                            info_dict.update({u'House_Type': content_detail_item_info})
                                        elif ind == 6:
                                            info_dict.update({u'PM_Fee': content_detail_item_info})
                                        elif ind == 7:
                                            info_dict.update({u'Total_Square_Meter': content_detail_item_info})
                                        elif ind == 8:
                                            info_dict.update({u'House_Num_on_Total': content_detail_item_info})
                                        elif ind == 9:
                                            info_dict.update({u'Year_Build': content_detail_item_info})
                                        elif ind == 10:
                                            info_dict.update({u'Plot_Ratio': content_detail_item_info})
                                        elif ind == 11:
                                            info_dict.update({u'Letting_Ratio': content_detail_item_info})
                                        elif ind == 12:
                                            info_dict.update({u'Parking_Lot': content_detail_item_info})
                                        elif ind == 13:
                                            info_dict.update({u'Greening_Ratio': content_detail_item_info})
                                        ind += 1
                                    info_dict.update({u'Additional_Content': content_detail.find(name="div",
                                                                                                 attrs={"class",
                                                                                                        "desc-cont"}).get_text()})
                            label = ""
                            if bs_t_2.find_all(name="div", attrs={"comm-mark clearfix"}) <> []:
                                for content_detail in bs_t_2.find_all(name="div", attrs={"comm-mark clearfix"}):
                                    for item in content_detail.find_all(name="a"):
                                        label += item.get_text() + "|"
                                info_dict.update({u'Label': label})

                            store_date(info_dict)
                            cnt += 1
                    else:
                        print("link exist!!")
            url_per_set.add(each)
            #print("Current_Processing_Percentage: %.2f" % (float(len(url_per_set))/float(len(url_set))) + "%")
    except Exception  as exp_msg:
        print(exp_msg)
        #print(ind_url)
    finally:
        print(GetCurrentTime())
        print("Done!!!!!!")