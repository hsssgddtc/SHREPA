# _*_ coding: utf-8 _*_

"""
Lianjia_Collection_Main_2017.py by shai
"""

import requests
import urllib2
import logging
import re
import sys
from datetime import datetime
from bs4 import BeautifulSoup

import utilities
import processor

global cur_house_hash_set
global cur_community_hash_set
global cur_community_link_set
global cur_link_repo
cur_link_repo_dict = {}
BASE_URL = "http://sh.lianjia.com"

#define the fetch process
class LianjiaFetcher(processor.Fetcher):
    def network_on(self):
        try:
            urllib2.urlopen('http://www.baidu.com', timeout=1)
            return True
        except urllib2.URLError as err:
            return False

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
        global cur_link_repo_dict

        cur_code, cur_url, cur_html = content
        bsObj = BeautifulSoup(cur_html, "html.parser")

        if content_type == "main_links":
            for content in bsObj.find_all(name="div", attrs={"id": "plateList"}):
                for item in content.find_all(name="a", gahref=re.compile(
                        "^((?!(district-nolimit)).)*$")):
                    DISTRICT_URL = BASE_URL + item.get("href")

                    logging.debug("Current District: " + item.get_text())
                    #logging.debug(DISTRICT_URL)

                    cur_link_repo_dict.update({"District": item.get_text()})

                    dis_code, content_dis = fetcher.working(DISTRICT_URL, None, 1, 3)
                    processor.html_parse(content_dis, "district_links")

        elif content_type == "district_links":
            for area_content in bsObj.find_all(name="div", attrs={"class": "level2 gio_plate"}):
                for area_item in area_content.find_all(name="a", gahref=re.compile("^((?!(plate-nolimit)).)*$")):
                    AREA_URL = BASE_URL + area_item.get("href")
                    logging.debug("Current Area: " + area_item.text)

                    cur_link_repo_dict.update({"Area": area_item.get_text()})

                    cur_code, content = fetcher.working(AREA_URL, None, 1, 3)
                    processor.html_parse(content, "area_links")


        elif content_type == "area_links":
            if bsObj.find_all(name="span", attrs={"class": "current"}) != []:
                current_page = bsObj.find_all(name="span", attrs={"class": "current"})[0].text
                logging.debug("Current Page: " + str(current_page))
                #print(cur_url)

                cur_link_repo_dict.update({"Page": current_page})
                cur_link_repo_dict.update({"URL": cur_url})
                cur_link_repo_dict.update({"Active_Flg": "Y"})

                #for keys, values in cur_link_repo_dict.items(): print(keys + " : " + values)

                if cur_url not in cur_link_repo:
                    dataset = saver.db_prep("link", cur_link_repo_dict)
                    saver.db_insert("link", dataset)
                    cur_link_repo.add(cur_link_repo_dict.get("URL"))
                else:
                    logging.debug("link exits")
            else:
                logging.debug("blank page")
                return None

            next_content = bsObj.find_all(name="div", attrs={"class": "c-pagination"})[0].find_all(name="a", attrs={
                "gahref": "results_next_page"})

            if next_content != []:
                next_page = BASE_URL + next_content[0].get("href")
                cur_code, content = fetcher.working(next_page, None, 1, 3)
                processor.html_parse(content, "area_links")
            else:
                exit

class LianjiaSaver(processor.Saver):
    def db_insert(self, type, dataset):
        cur = self.conn.cursor()
        cur.execute(
                "INSERT INTO link_repo(District, Area, Page, URL, Active_Flg) "
                "VALUES (%s,%s,%s,%s,%s)",
                (dataset))

        cur.connection.commit()

    def db_delete(self, type, data):
        cur = self.conn.cursor()
        if type == "community_link":
            cur.execute("Delete from community_info_saf where Community_Link=%s", data)
        elif type == "link_repo":
            cur.execute("Truncate table link_repo")

        cur.connection.commit()

if __name__ == "__main__":
    """
    main process
    """
    if len(sys.argv)>1 and sys.argv[1] == 'log':
        utilities.SetupLogging("log")
    else:
        utilities.SetupLogging("console")
    # logger.debug("Fetching Start: %s", datetime.now())

    utilities.HandleDaemon("create")
    try:
        fetcher = LianjiaFetcher(critical_max_repeat=3, critical_sleep_time=0)
        processor = LianjiaParser(max_deep=1, max_repeat=3)
        saver = LianjiaSaver(save_type="db", db_info=utilities.CONFIG_DB_INFO)

        network_check = fetcher.network_on()


        if network_check:
            House_Info_Type_Name = "ershoufang"

            cur_code, content = fetcher.working(BASE_URL + "/" + House_Info_Type_Name, None, 1, 3)

            if len(sys.argv)>2 and sys.argv[2]=='refresh':
                saver.db_delete("linl_repo",None)
                processor.html_parse(content, "main_links")

    except Exception as excep:
        logging.debug("Exception: %s", excep)
        logging.exception(excep)
        raise
        #traceback.print_exc()
    finally:
        logging.debug("Fetcher end: %s", datetime.now())
        utilities.HandleDaemon("delete")
