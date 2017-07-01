# -*- coding:utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import re
import pymysql
import time
import random

global BASE_URL
BASE_URL = 'http://sh.lianjia.com'

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
    base_url = BASE_URL + '/' + type + '/d'
    # chengjiao: 1~2413 ; ershou: 1~1941
    main_url = base_url + str(number)
    return main_url


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

if __name__ == '__main__':
    orig_url = "http://sh.lianjia.com/chengjiao/sh4277188.html"


    req = urllib2.Request(orig_url,headers=hds[random.randint(0, len(hds) - 1)])
    html = urllib2.urlopen(req, timeout=10)
    bsObj = BeautifulSoup(html, "html.parser")

    print(bsObj)

    #for content in bs_t_1.find_all(name="div", attrs={"_soj": "xqlb"}):
    #    info_dict = {}
    #    ind_url = BASE_URL + content.find(name="a", attrs={"title": True}).get("href")
    #    # print(ind_url)
    #    # if cnt % 80 == 0:
    #    #    time.sleep(60)
    #    if ind_url not in link_set:
    #        info_dict.update({u'Community_Name': content.find(name="a",
    #                                                          attrs={"title": True}).get(
    #            "title")})
    #        info_dict.update({u'Quoted_Price': content.find(
    #            name="strong").get_text().replace("\r", "").replace("\n", "")})
    #        info_dict.update({u'Chain_Increase': content.find(name="p", attrs={
    #            "class": "price-txt"}).get_text().replace("\r", "")
    #                         .replace("\n", "").replace("↑", "+").replace("↓", "-")})
    #        info_dict.update({u'Community_Link': ind_url})
    #        # print("*********************")
    #        sleep_period = random.randint(2, 7)
    #        print("randomly sleep for " + str(sleep_period) + " seconds")
    #        time.sleep(sleep_period)
#
    #        bs_t_2 = getBSobj(ind_url)
    #        ind = 0
    #        for content_detail in bs_t_2.find_all(name="div", attrs={
    #            "class": "border-info comm-detail"}):
    #            for content_detail_item in content_detail.find_all(name="dd"):
    #                content_detail_item_info = content_detail_item.get_text().replace("\r",
    #                                                                                  "").replace(
    #                    "\n", "").replace("                        ",
    #                                      " ").lstrip()
    #                # print(content_detail_item_info)
    #                if ind == 1:
    #                    if content_detail_item_info.find(" ") > 0:
    #                        info_dict.update({u'District': content_detail_item_info[
    #                                                       :content_detail_item_info.index(
    #                                                           " ")]})
    #                        info_dict.update({u'Area': content_detail_item_info[
    #                                                   content_detail_item_info.index(
    #                                                       " ") + 1:]})
    #                    else:
    #                        info_dict.update({u'District': content_detail_item_info})
    #                elif ind == 2:
    #                    info_dict.update({u'Address': content_detail_item_info})
    #                elif ind == 3:
    #                    info_dict.update({u'Developer': content_detail_item_info})
    #                elif ind == 4:
    #                    info_dict.update({u'PM_Company': content_detail_item_info})
    #                elif ind == 5:
    #                    info_dict.update({u'House_Type': content_detail_item_info})
    #                elif ind == 6:
    #                    info_dict.update({u'PM_Fee': content_detail_item_info})
    #                elif ind == 7:
    #                    info_dict.update({u'Total_Square_Meter': content_detail_item_info})
    #                elif ind == 8:
    #                    info_dict.update({u'House_Num_on_Total': content_detail_item_info})
    #                elif ind == 9:
    #                    info_dict.update({u'Year_Build': content_detail_item_info})
    #                elif ind == 10:
    #                    info_dict.update({u'Plot_Ratio': content_detail_item_info})
    #                elif ind == 11:
    #                    info_dict.update({u'Letting_Ratio': content_detail_item_info})
    #                elif ind == 12:
    #                    info_dict.update({u'Parking_Lot': content_detail_item_info})
    #                elif ind == 13:
    #                    info_dict.update({u'Greening_Ratio': content_detail_item_info})
    #                ind += 1
    #            info_dict.update({u'Additional_Content': content_detail.find(name="div",
    #                                                                         attrs={"class",
    #                                                                                "desc-cont"}).get_text()})
    #        label = ""
    #        for content_detail in bs_t_2.find_all(name="div", attrs={"comm-mark clearfix"}):
    #            for item in content_detail.find_all(name="a"):
    #                label += item.get_text() + "|"
    #        info_dict.update({u'Label': label})
#
    #    for each in info_dict:
    #        print(info_dict[each])
    #BASE_URL = "http://shanghai.anjuke.com/school/"
    #DISTRICT = ['pudong', 'minhang', 'xuhui', 'putuo', 'changning', 'jingan', 'huangpu', 'luwan', 'hongkou', 'zhabei',
    #            'yangpu', 'baoshan', 'songjiang', 'jiading', 'qingpu', 'fengxian', 'jinshan', 'chongming',
    #            'shanghaizhoubian']
    #url_set = set()
    #url_per_set = set()
    #DISTRICT = ['pudong']
#
    #for each in DISTRICT:
    #    print("Current District: " + each)
    #    district_url = BASE_URL + each
    #    url_set.add(district_url)
#
    #    bs_t_1 = getBSobj(district_url)
#
    #    for content in bs_t_1.find_all(name="div", attrs={"class":"multi-page"}):
    #       for item in content.find_all(name="a"):
    #           url_set.add(item.get("href"))
    #    print("***********************")
#
    #for each in url_set:
    #    bs_t_1 = getBSobj(each)
    #    for content in bs_t_1.find_all(name="a", attrs={"class":"school_name"}):
    #        school_url = content.get("href")
    #        #print(school_url)
#
    #        bs_t_2 = getBSobj(school_url)
    #        #print(bs_t_2.find("h1").get_text())
    #        #break
#
    #        for content in bs_t_2.find_all(name="div", attrs={"class":"schprofile"}):
    #           print(content)
    #           print(getSubstring_colon(content.find(name="li", attrs={"class": "averagemoney"}).get_text().encode("utf-8")))
    #           print(getSubstring_colon(content.find_all(name="li", attrs={"class": "Ld1com"})[0].get_text().encode("utf-8")))
    #           print(getSubstring_colon(content.find_all(name="li", attrs={"class": "Ld1com"})[1].get_text().encode("utf-8")))
    #           print(getSubstring_colon(content.find_all(name="li", attrs={"class": "Ld1com"})[2].get_text().encode("utf-8")))
    #           #getSubstring_line(getSubstring_colon(content.find_all(name="li", attrs={"class": "Ld1com"})[3].get_text().encode("utf-8").replace("\r","").replace("\n","").replace(" ","")))
    #           print(getSubstring_colon(content.find_all(name="li", attrs={"class": "Ld1com"})[4].get_text().encode("utf-8")))
    #           print(content.find(name="a", attrs={"class":"Ld1num"}, href=re.compile("comm")).get("href"))
    #           print(content.find(name="a", id="Ld1a1").get("href"))
    #           print(content.find(name="a", id="Ld1a2").get("href"))
    #           print(content.find_all(name="a", attrs={"class": "Ld1num"})[0].get_text().encode("utf-8"))
    #           print(content.find_all(name="a", attrs={"class": "Ld1num"})[1].get_text().encode("utf-8"))
    #           if content.find(name="div", attrs={"class": "Ld2"}) is not None:
    #               print(content.find(name="div", attrs={"class": "Ld2"}).find(name="p", attrs={
    #                   "class": "introduction"}).get_text())
    #           if content.find(name="div", attrs={"class": "Ld3"}) is not None:
    #               print(content.find(name="div", attrs={"class": "Ld3"}).find(name="p", attrs={
    #                   "class": "introduction"}).get_text())
#
    #        exit(0)
#
    #        print("****************************")
    #    break
    #for content in bs_t_1.find_all(name="a"):
    #    print(content)

    #for content in bs_t_1.find_all(name="div", attrs={"class":"schprofile"}):
    #    #print(content)
    #    print(content.find(name="li", attrs={"class": "averagemoney"}).get_text())
    #    print(content.find_all(name="li", attrs={"class": "Ld1com"})[0].get_text())
    #    print(content.find_all(name="li", attrs={"class": "Ld1com"})[1].get_text())
    #    print(content.find_all(name="li", attrs={"class": "Ld1com"})[2].get_text())
    #    print(content.find_all(name="li", attrs={"class": "Ld1com"})[3].get_text().encode("utf-8").replace("\r","").replace("\n","").replace(" ",""))
    #    print(content.find_all(name="li", attrs={"class": "Ld1com"})[4].get_text())
    #    print(content.find(name="a", attrs={"class":"Ld1num"}, href=re.compile("comm")).get("href"))
    #    print(content.find(name="a", id="Ld1a1").get("href"))
    #    print(content.find(name="a", id="Ld1a2").get("href"))
    #    print(content.find(name="div", attrs={"class":"Ld2"}).find(name="p", attrs={"class":"introduction"}).get_text())
    #    print(content.find(name="div", attrs={"class": "Ld3"}).find(name="p", attrs={"class": "introduction"}).get_text())
    #print(bs_t_1)