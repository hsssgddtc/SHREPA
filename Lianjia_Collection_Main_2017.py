# _*_ coding: utf-8 _*_

import requests
import random

import utilities
import processor

url_house_info='http://sh.lianjia.com/ershoufang/sh4509559.html'

#define the fetch process
#class HouseFetcher(processor.Fetcher):
#
#    def url_fetch(self, url, keys, critical, fetch_repeat):
#        headers = {"User-Agent": utilities.make_random_useragent("pc"), "Accept-Encoding": "gzip"}
#        response = requests.get(url, headers=headers, timeout=10)
#
#        content = (response.status_code, response.url, response.text)
#
#        return 1, content






if __name__ == "__main__":
    """
    main process
    """
    fetcher = processor.Fetcher(critical_max_repeat=3, critical_sleep_time=0)

    a,b = fetcher.working(url_house_info, None, 1, 3)

    print(b[2])

    #result = fetcher.url_fetch(url_house_info)

    #print(result)