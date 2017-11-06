# _*_ coding: utf-8 _*_

"""
pro_fetch.py by shai
"""
import requests
import logging
import random
import time

from utilities import *

class Fetcher(object):
    """
    class of Fetcher, must include function url_fetch()
    """

    def __init__(self, normal_max_repeat=3, normal_sleep_time=3, critical_max_repeat=10, critical_sleep_time=10):
        """
        constructor
        """
        self.normal_max_repeat = normal_max_repeat
        self.normal_sleep_time = normal_sleep_time
        self.critical_max_repeat = critical_max_repeat
        self.critical_sleep_time = critical_sleep_time
        return

    def url_fetch(self, url, keys, critical, fetch_repeat):
        """
        fetch the content of a url, function can be rewrite, parameters and return refer to self.working()
        """

        #get response based on headers
        headers = {
            "User-Agent": make_random_useragent(),
            "Accept-Encoding": "gzip"
        }
        response = requests.get(url, params=None, data=None, headers=headers, cookies=None, timeout=(3.05, 10))
        if response.history:
            logging.debug("Fetcher redirect: url=%s", url)

        content = (response.status_code, response.url, response.text)
        return 1, content

    def working(self, url, keys, critical, fetch_repeat):
        """
        working function, must "try, except" and call self.url_fetch(), don't change parameters and return
        :param url: the url, which need to be fetched
        :param keys: some information of this url, which can be used in this function
        :param critical: the critical flag of this url, which can be used in this function
        :param fetch_repeat: the fetch repeat time of this url, if fetch_repeat >= self.*_max_repeat, return code = -1
        :return (code, content): code can be -1(fetch failed), 0(need to repeat), 1(fetch success), 
                                content must be a list or tuple 
        """
        logging.debug("Fetcher start: url=%s, keys=%s, critical=%s, fetch_repeat=%s", url, keys, critical, fetch_repeat)
        time.sleep(random.randint(0, self.normal_sleep_time if (not critical) else self.critical_sleep_time))

        try:
            code, content = self.url_fetch(url, keys, critical, fetch_repeat)
        except Exception as exp_msg:
            if ((not critical) and (fetch_repeat >= self.normal_max_repeat)) \
                    or (critical and (fetch_repeat >= self.critical_max_repeat)):
                code, content = -1, None
                logging.error("Fetcher error: %s, url=%s, keys=%s, critical=%s, fetch_repeat=%s", exp_msg, url, keys, critical, fetch_repeat)
            else:
                code, content = 0, None
                logging.debug("Fecher repeat: %s, url=%s, keys=%s, critical=%s, fetch_repeat=%s", exp_msg, url, keys, critical, fetch_repeat)


        logging.debug("Fetcher end: code=%s, url=%s", code, url)
        return code, content