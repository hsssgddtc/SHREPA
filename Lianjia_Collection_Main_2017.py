# _*_ coding: utf-8 _*_

import requests


import utilities

url_house_info='http://sh.lianjia.com/ershoufang/sh4509559.html'

#define the fetch process
class HouseFetcher():

    def url_fetch(self, url):
        headers = {"User-Agent": utilities.make_random_useragent("pc"), "Accept-Encoding": "gzip"}
        response = requests.get(url, headers=headers, timeout=10)

        try:
            if response.status_code == 200:
                return response.text
        except Exception as exp_msg:
            print(exp_msg)



if __name__ == "__main__":
    """
    main process
    """
    fetcher = HouseFetcher()

    result = fetcher.url_fetch(url_house_info)

    print(result)