# _*_ coding: utf-8 _*_

import requests
import random
import urllib2
from bs4 import BeautifulSoup

import utilities
import processor

url_house_info='http://sh.lianjia.com/ershoufang/sh4509559.html'

#define the fetch process
class LianjiaFetcher(processor.Fetcher):

    def url_fetch(self, url, keys, critical, fetch_repeat):
        headers = {"User-Agent": utilities.make_random_useragent("pc"), "Accept-Encoding": "gzip"}
        response = requests.get(url, headers=headers, timeout=10)

        content = (response.status_code, response.url, response.text)
        return 1, content

class LianjiaParser(processor.Parser):
    def html_parse(self, content):
        """
        :param content: 
        :return: 
        """
        url_list, content_dict = [], {}

        cur_code, cur_url, cur_html = content
        bsObj = BeautifulSoup(cur_html, "html.parser")

        content_dict.update({"House_Title": bsObj.find_all(name="div", attrs={"class": "header-row2"})[0].text.strip()})
        content_dict.update({"Listing_Price": bsObj.find_all(name="span", attrs={"class": "price-num"})[0].text})
        content_dict.update(
            {"Quoted_Price": bsObj.find_all(name="p", attrs={"class": "price-unit-num"})[0].find_all(name="span")[0].text})
        content_dict.update(
            {"Year_Build": bsObj.find_all(name="li", attrs={"class": "main-item u-tr"})[0].find_all(name="p", attrs={
                "class": "u-fz12"})[
                0].text.strip()})
        content_dict.update(
            {"Ring_Line":
                 bsObj.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(name="span",
                                                                                                         attrs={
                                                                                                             "class": "item-cell"})[
                     5].text})
        community_info = \
            bsObj.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(name="span", attrs={
                "class": "item-cell"})[7].text.encode("utf-8").strip()
        content_dict.update(
            {"Community_Name": community_info[:community_info.find(" ")]})
        content_dict.update(
            {"District": community_info[community_info.find("(") + 1:community_info.find(" ", community_info.find("("))]})
        content_dict.update(
            {"Area": community_info[community_info.find(" ", community_info.find("(")) + 2:community_info.find(")")]})
        content_dict.update({"Address":
                                    bsObj.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(
                                        name="span", attrs={
                                            "class": "item-cell"})[9].text.encode("utf-8").strip()})

        Seriel_Number = \
        bsObj.find_all(name="ul", attrs={"class": "maininfo-minor maininfo-item"})[0].find_all(name="span", attrs={
            "class": "item-cell"})[13].text.encode("utf-8").replace('\n', '').replace(' ', '')[:9]
        House_Link = "sh.lianjia.com/ershoufang/" + Seriel_Number + ".html"
        content_dict.update(
            {"Seriel_Number": Seriel_Number})
        content_dict.update(
            {"House_Link": House_Link})
        content_dict.update(
            {"Structure_Type": bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[1].find_all(name="span", attrs={
                "class": "item-cell"})[1].text.strip()})
        content_dict.update(
            {"Elevator": bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[1].find_all(name="span", attrs={
                "class": "item-cell"})[3].text.strip()})
        content_dict.update(
            {"Square_Meter": bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[1].find_all(name="span", attrs={
                "class": "item-cell"})[5].text.strip()})
        content_dict.update(
            {"Heating_Type": bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[1].find_all(name="span", attrs={
                "class": "item-cell"})[7].text.strip()})
        content_dict.update(
            {"Floor_Number": bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[2].find_all(name="span", attrs={
                "class": "item-cell"})[1].text.strip()})
        content_dict.update(
            {"Decoration_Level": bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[2].find_all(name="span", attrs={
                "class": "item-cell"})[3].text.strip()})
        content_dict.update(
            {"Orientation_Type": bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[2].find_all(name="span", attrs={
                "class": "item-cell"})[5].text.strip()})
        content_dict.update(
            {"Parking_Place": bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[2].find_all(name="span", attrs={
                "class": "item-cell"})[7].text.strip()})
        content_dict.update(
            {"Last_Trade_Date": bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[4].find_all(name="span", attrs={
                "class": "item-cell"})[1].text.strip()})
        content_dict.update(
            {"Restriction_Type": bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[4].find_all(name="span", attrs={
                "class": "item-cell"})[3].text.strip()})
        content_dict.update(
            {"Trade_Reason": bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[5].find_all(name="span", attrs={
                "class": "item-cell"})[1].text.strip()})
        content_dict.update(
            {"House_Type_Name": bsObj.find_all(name="ul", attrs={"class": "baseinfo-tb"})[5].find_all(name="span", attrs={
                "class": "item-cell"})[3].text.strip()})
        content_dict.update(
            {"Num_of_Visit_7": bsObj.find_all(name="div", attrs={"id": "kanfangListVue"})[0].find_all(name="look-list")[
                0].get("count7").encode("utf-8")})
        content_dict.update(
            {"Num_of_Visit_90": bsObj.find_all(name="div", attrs={"id": "kanfangListVue"})[0].find_all(name="look-list")[
                0].get("count90").encode("utf-8")})

        if len(bsObj.find_all(name="div", attrs={"id": "js-owner-comment"})) > 0:
            content_dict.update(
                {"Owner_My_Story": bsObj.find_all(name="div", attrs={"id": "js-owner-comment"})[0].find_all(name="li",
                                                                                                             attrs={
                                                                                                                 "class": "comment-item"})[
                                       0].text.encode("utf-8").replace('\n', '').replace(' ', '')[12:]})

            content_dict.update(
                {"Owner_Decoration": bsObj.find_all(name="div", attrs={"id": "js-owner-comment"})[0].find_all(name="li",
                                                                                                               attrs={
                                                                                                                   "class": "comment-item"})[
                                         1].text.encode("utf-8").replace('\n', '').replace(' ', '')[12:]})

            content_dict.update(
                {"Owner_House_Feature": bsObj.find_all(name="div", attrs={"id": "js-owner-comment"})[0].find_all(name="li",
                                                                                                                  attrs={
                                                                                                                      "class": "comment-item"})[
                                            2].text.encode("utf-8").replace('\n', '').replace(' ', '')[12:]})
        return 1, url_list, content_dict




if __name__ == "__main__":
    """
    main process
    """
    fetcher = LianjiaFetcher(critical_max_repeat=3, critical_sleep_time=0)
    processor = LianjiaParser(max_deep=1, max_repeat=3)


    cur_code,content = fetcher.working(url_house_info, None, 1, 3)
    house_info = processor.html_parse(content)


    #result = fetcher.url_fetch(url_house_info)

    for keys, values in house_info[2].items(): print(keys+" : "+values)