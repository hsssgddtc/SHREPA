# -*- coding:utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import re
import pymysql
import time
import random

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

def url_set_gen():
    url_set = set()
    BASE_URL = "http://shanghai.anjuke.com/school/"
    DISTRICT = ['minhang', 'xuhui', 'putuo', 'changning', 'jingan', 'huangpu', 'luwan', 'hongkou', 'zhabei',
                'yangpu', 'baoshan', 'songjiang', 'jiading', 'qingpu', 'fengxian', 'jinshan', 'chongming',
                'shanghaizhoubian','pudong']
    #DISTRICT = ['pudong']
    for each in DISTRICT:
        print("Current District: " + each)
        district_url = BASE_URL + each
        url_set.add(district_url)

        bs_t_1 = getBSobj(district_url)

        for content in bs_t_1.find_all(name="div", attrs={"class": "multi-page"}):
            for item in content.find_all(name="a"):
                url_set.add(item.get("href"))
        print("***********************")
    return(url_set)

def get_links():
    cur.execute("SELECT School_Link FROM school_info_saf")
    orig_set = set(link[0] for link in cur)
    return (orig_set)

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

def store_date(info_dict):
    info_list=[u'School_Name',u'School_Type',u'School_Level',u'School_Character',u'School_Distrct_Quoted_Price',u'District'
        ,u'Area',u'Address',u'School_Phone_Num',u'House_Num_on_Sold',u'Community_Num_on_Total',u'School_Admission',u'School_Introduction'
        ,u'School_Link', u'Community_Link', u'District_Link', u'Area_Link']

    t=[]
    for column in info_list:
        if column in info_dict:
            t.append(info_dict[column])
        else:
            t.append(None)

    t=tuple(t)

    cur.execute("INSERT INTO school_info_saf(School_Name,School_Type,School_Level,School_Character,School_Distrct_Quoted_Price,District \
        ,Area,Address,School_Phone_Num,House_Num_on_Sold,Community_Num_on_Total,School_Admission,School_Introduction \
        ,School_Link, Community_Link, District_Link, Area_Link ) \
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", \
                (t))

    cur.connection.commit()
    print("insert data done")

def getContent(BeautifulSoup):
    info_dict = {}
    try:
        for content in BeautifulSoup.find_all(name="a", attrs={"class": "school_name"}):
            school_url = content.get("href")
            print(school_url)

            sleep_period = random.randint(2, 7)
            print("randomly sleep for " + str(sleep_period) + " seconds")
            time.sleep(sleep_period)

            bs_t_1 = getBSobj(school_url)

            info_dict.update({u'School_Name': bs_t_1.find("h1").get_text()})
            info_dict.update({u'School_Link': school_url})

            if bs_t_1.find_all(name="div", attrs={"class": "schprofile"}) == []:
                pass
            else:
                for content in bs_t_1.find_all(name="div", attrs={"class": "schprofile"}):
                    # print(content)
                    info_dict.update({u'School_Type': getSubstring_colon(content.find_all(name="li", attrs={"class": "Ld1com"})[0].get_text().encode("utf-8"))})
                    info_dict.update({u'School_Level': getSubstring_colon(
                        content.find_all(name="li", attrs={"class": "Ld1com"})[1].get_text().encode("utf-8"))})
                    info_dict.update({u'School_Character': getSubstring_colon(
                        content.find_all(name="li", attrs={"class": "Ld1com"})[2].get_text().encode("utf-8"))})
                    info_dict.update({u'School_Distrct_Quoted_Price': getSubstring_colon(
                        content.find(name="li", attrs={"class": "averagemoney"}).get_text().encode("utf-8"))})
                    info_dict.update({u'District': getSubstring_line(getSubstring_colon(
                        content.find_all(name="li", attrs={"class": "Ld1com"})[3].get_text().encode("utf-8").replace("\r","").replace("\n","").replace(" ","")),1)})
                    info_dict.update({u'Area': getSubstring_line(getSubstring_colon(
                        content.find_all(name="li", attrs={"class": "Ld1com"})[3].get_text().encode("utf-8").replace("\r","").replace("\n","").replace(" ","")), 2)})
                    info_dict.update({u'Address': getSubstring_line(getSubstring_colon(
                        content.find_all(name="li", attrs={"class": "Ld1com"})[3].get_text().encode("utf-8").replace("\r","").replace("\n","").replace(" ","")), 3)})
                    info_dict.update({u'School_Phone_Num': getSubstring_colon(
                        content.find_all(name="li", attrs={"class": "Ld1com"})[4].get_text().encode("utf-8"))})
                    info_dict.update({u'House_Num_on_Sold': content.find_all(name="a", attrs={"class": "Ld1num"})[0].get_text().encode("utf-8")})
                    info_dict.update({u'Community_Num_on_Total': content.find_all(name="a", attrs={"class": "Ld1num"})[
                        1].get_text().encode("utf-8")})
                    School_Admission = School_Introduction = "N/A"
                    if content.find(name="div", attrs={"class": "Ld2"}) is not None:
                        School_Admission = content.find(name="div", attrs={"class": "Ld2"}).find(name="p", attrs={
                            "class": "introduction"}).get_text()

                    if content.find(name="div", attrs={"class": "Ld3"}) is not None:
                        School_Introduction = content.find(name="div", attrs={"class": "Ld3"}).find(name="p", attrs={
                            "class": "introduction"}).get_text()
                    info_dict.update({u'School_Admission': School_Admission})
                    info_dict.update({u'School_Introduction': School_Introduction})
                    info_dict.update({u'Community_Link': content.find(name="a", attrs={"class": "Ld1num"}, href=re.compile("comm")).get("href")})
                    info_dict.update({u'District_Link': content.find(name="a", id="Ld1a1").get("href")})
                    info_dict.update({u'Area_Link': content.find(name="a", id="Ld1a2").get("href")})

                    store_date(info_dict)
                #exit(0)

            #print(info_dict)
    except urllib2.HTTPError as e:
        return None
    return info_dict

def GetCurrentTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

if __name__ == '__main__':
    existing_url_set = get_links()
    url_per_set = set()
    url_set = url_set_gen()

    try:
        for each in url_set:
            if each not in existing_url_set:

                bs_t_1 = getBSobj(each)
                getContent(bs_t_1)

    except Exception  as exp_msg:
        print(exp_msg)
        print(each)
    finally:
        print(GetCurrentTime())
        print("Done!!!!!!")