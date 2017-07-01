#!/usr/bin/python
#coding:utf-8

import urllib2

from __builtin__ import float
from bs4 import BeautifulSoup
import re
import pymysql
import time
import random
import sys

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

conn = pymysql.connect(host='127.0.0.1', user='shai', passwd='Thermo2014!', db='SHREPA', charset='utf8')
cur = conn.cursor()
cur.execute("USE SHREPA")



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

def insert_house_data(house_info_dict):
    house_info_list=[u'House_Title',u'House_Type_Name',u'Structure_Type',u'Decoration_Level'
        ,u'Orientation_Type',u'Restriction_Type',u'Listing_Price',u'Square_Meter',u'Quoted_Price'
        ,u'Floor_Number',u'Year_Build',u'District',u'Area',u'Address',u'Community_Name'
        ,u'Ring_Line',u'Elevator',u'Heating_Type',u'Keys_Flag',u'Num_of_Visit_7',u'Num_of_Visit_90',u'Last_Trade_Date'
        ,u'Owner_My_Story', u'Owner_Decoration', u'Owner_House_Feature',u'Seriel_Number',u'House_Link']

    t=[]

    for column in house_info_list:
        if column in house_info_dict:
            t.append(house_info_dict[column])
            #print(house_info_dict[column])
        else:
            t.append(None)

    t=tuple(t)

    cur.execute("INSERT INTO house_info_saf_2017(House_Title, House_Type_Name, Structure_Type, Decoration_Level, Orientation_Type,"
                "Restriction_Type,Listing_Price, Square_Meter, Quoted_Price, Floor_Number, Year_Build, District,"
                "Area, Address, Community_Name, Ring_Line, Elevator, Heating_Type, Keys_Flag,"
                "Num_of_Visit_7, Num_of_Visit_90, Last_Trade_Date, "
                "Owner_My_Story, Owner_Decoration, Owner_House_Feature, Seriel_Number, House_Link) "
               "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (t))

    cur.connection.commit()

    print("insert house data done")

if __name__ == '__main__':
    #house_link='http://sh.lianjia.com/ershoufang/sh4669593.html'
    #house_link = 'http://sh.lianjia.com/ershoufang/sh4553009.html'
    house_link='http://sh.lianjia.com/ershoufang/sh4509559.html'

    bs_t_1 = getBSobj(house_link)

    house_info_dict = {}


    house_info_dict.update({"House_Title":bs_t_1.find_all(name="div", attrs={"class": "header-row2"})[0].text.strip()})
    house_info_dict.update({"Listing_Price":bs_t_1.find_all(name="span", attrs={"class": "price-num"})[0].text})
    house_info_dict.update({"Quoted_Price": bs_t_1.find_all(name="p", attrs={"class": "price-unit-num"})[0].find_all(name="span")[0].text})
    house_info_dict.update(
        {"Year_Build":bs_t_1.find_all(name="li", attrs={"class": "main-item u-tr"})[0].find_all(name="p", attrs={"class": "u-fz12"})[
        0].text.strip()})
    house_info_dict.update(
        {"Ring_Line":bs_t_1.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(name="span", attrs={"class": "item-cell"})[5].text})
    community_info = \
    bs_t_1.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(name="span", attrs={
        "class": "item-cell"})[7].text.encode("utf-8").strip()
    house_info_dict.update(
        {"Community_Name":community_info[:community_info.find(" ")]})
    house_info_dict.update(
        {"District":community_info[community_info.find("(")+1:community_info.find(" ",community_info.find("("))]})
    house_info_dict.update(
        {"Area":community_info[community_info.find(" ", community_info.find("("))+2:community_info.find(")")]})
    house_info_dict.update({"Address":bs_t_1.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(name="span", attrs={
        "class": "item-cell"})[9].text.encode("utf-8").strip()})

    Seriel_Number=bs_t_1.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(name="span", attrs={
        "class": "item-cell"})[13].text.encode("utf-8").replace('\n','').replace(' ','')[:9]
    House_Link="sh.lianjia.com/ershoufang/"+Seriel_Number+".html"
    house_info_dict.update(
        {"Seriel_Number":Seriel_Number})
    house_info_dict.update(
        {"House_Link": House_Link})
    house_info_dict.update(
        {"Structure_Type":bs_t_1.find_all(name="ul", attrs={"class": "baseinfo-tb"})[1].find_all(name="span", attrs={
        "class": "item-cell"})[1].text.strip()})
    house_info_dict.update(
        {"Elevator":bs_t_1.find_all(name="ul", attrs={"class": "baseinfo-tb"})[1].find_all(name="span", attrs={
        "class": "item-cell"})[3].text.strip()})
    house_info_dict.update(
        {"Square_Meter":bs_t_1.find_all(name="ul", attrs={"class": "baseinfo-tb"})[1].find_all(name="span", attrs={
        "class": "item-cell"})[5].text.strip()})
    house_info_dict.update(
        {"Heating_Type":bs_t_1.find_all(name="ul", attrs={"class": "baseinfo-tb"})[1].find_all(name="span", attrs={
        "class": "item-cell"})[7].text.strip()})
    house_info_dict.update(
        {"Floor_Number":bs_t_1.find_all(name="ul", attrs={"class": "baseinfo-tb"})[2].find_all(name="span", attrs={
        "class": "item-cell"})[1].text.strip()})
    house_info_dict.update(
        {"Decoration_Level":bs_t_1.find_all(name="ul", attrs={"class": "baseinfo-tb"})[2].find_all(name="span", attrs={
        "class": "item-cell"})[3].text.strip()})
    house_info_dict.update(
        {"Orientation_Type":bs_t_1.find_all(name="ul", attrs={"class": "baseinfo-tb"})[2].find_all(name="span", attrs={
        "class": "item-cell"})[5].text.strip()})
    house_info_dict.update(
        {"Parking_Place":bs_t_1.find_all(name="ul", attrs={"class": "baseinfo-tb"})[2].find_all(name="span", attrs={
        "class": "item-cell"})[7].text.strip()})
    house_info_dict.update(
        {"Last_Trade_Date":bs_t_1.find_all(name="ul", attrs={"class": "baseinfo-tb"})[4].find_all(name="span", attrs={
        "class": "item-cell"})[1].text.strip()})
    house_info_dict.update(
        {"Restriction_Type":bs_t_1.find_all(name="ul", attrs={"class": "baseinfo-tb"})[4].find_all(name="span", attrs={
        "class": "item-cell"})[3].text.strip()})
    house_info_dict.update(
        {"Trade_Reason":bs_t_1.find_all(name="ul", attrs={"class": "baseinfo-tb"})[5].find_all(name="span", attrs={
        "class": "item-cell"})[1].text.strip()})
    house_info_dict.update(
        {"House_Type_Name":bs_t_1.find_all(name="ul", attrs={"class": "baseinfo-tb"})[5].find_all(name="span", attrs={
        "class": "item-cell"})[3].text.strip()})
    house_info_dict.update(
        {"Num_of_Visit_7":bs_t_1.find_all(name="div", attrs={"id":"kanfangListVue"})[0].find_all(name="look-list")[0].get("count7").encode("utf-8")})
    house_info_dict.update(
        {"Num_of_Visit_90":bs_t_1.find_all(name="div", attrs={"id": "kanfangListVue"})[0].find_all(name="look-list")[0].get("count90").encode("utf-8")})




    if len(bs_t_1.find_all(name="div", attrs={"id": "js-owner-comment"}))>0:
        house_info_dict.update(
            {"Owner_My_Story": bs_t_1.find_all(name="div", attrs={"id": "js-owner-comment"})[0].find_all(name="li",
                                                                                                         attrs={
                                                                                                             "class": "comment-item"})[
                                   0].text.encode("utf-8").replace('\n', '').replace(' ', '')[12:]})

        house_info_dict.update(
            {"Owner_Decoration": bs_t_1.find_all(name="div", attrs={"id": "js-owner-comment"})[0].find_all(name="li",
                                                                                                           attrs={
                                                                                                               "class": "comment-item"})[
                                     1].text.encode("utf-8").replace('\n', '').replace(' ', '')[12:]})

        house_info_dict.update(
            {"Owner_House_Feature": bs_t_1.find_all(name="div", attrs={"id": "js-owner-comment"})[0].find_all(name="li",
                                                                                                              attrs={
                                                                                                                  "class": "comment-item"})[
                                        2].text.encode("utf-8").replace('\n', '').replace(' ', '')[12:]})
    #print(house_info_dict)

    #print(type(bs_t_1.find_all(name="div", attrs={"id":"kanfangListVue"})[0].find_all(name="look-list")[0].get("count7").encode("utf-8")))

    #for keys, values in house_info_dict.items(): print(keys+":"+values)

    #print(bs_t_1.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(name="a", attrs={"class": "u-link"})[0].get("href"))
    #print(bs_t_1.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(name="a", attrs={"class": "u-link"})[1].get("href"))
    #print(bs_t_1.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(name="a", attrs={"class": "u-link"})[2].get("href"))
    #print("test")
    insert_house_data(house_info_dict)

