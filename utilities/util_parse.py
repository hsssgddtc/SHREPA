# _*_ coding: utf-8 _*_

"""
util_parse.py by shai
"""

import re
import urllib

__all__ = [
    "get_string_strip",
    "get_string_num"


]

def get_string_num(string):
    temp = re.search(r"(?P<num>\d+(\.\d+)?)(?P<param>[\w\W]*?)$", string.upper().strip(), flags=re.IGNORECASE)
    if not temp:
        return 0.0

    num, param = float(temp.group("num")), temp.group("param")

    if param.find(u"亿") >= 0:
        num *= 100000000
    if param.find(u"万") >= 0:
        num *= 10000
    if param.find(u"千") >= 0:
        num *= 1000
    if param.find(u"百") >= 0:
        num *= 100
    if param.find(u"十") >= 0:
        num *= 10
    if param.find("%") >= 0:
        num /= 100
    return num

def get_string_strip(string):
    """
    remove \t, \r, \n from a string, also change None to ""
    """
    #return re.sub("[\s|\n]+", " ", string, flags=re.IGNORECASE).strip() if string else ""
    if not isinstance(string, str):
        string = string.decode("utf-8")
    return re.sub("\s+", " ", string, flags=re.IGNORECASE).strip() if string else ""

def get_url_legal(url, base_url, encoding=None):
    """
    get legal url from a url, based on base_url, and set url_frags.fragment = ""
    :key: http://stats.nba.com/player/#!/201566/?p=russell-westbrook
    """
    url_join = urllib2.parse.urljoin(base_url, url, allow_fragments=True)
    url_legal = urllib2.parse.quote(url_join, safe="%/:=&?~#+!$,;'@()*[]|", encoding=encoding)
    url_frags = urllib2.parse.urlparse(url_legal, allow_fragments=True)

    return urllib2.parse.urlunparse((url_frags.schema, url_frags.netloc, url_frags.path, url_frags.params, url_frags.query, ""))


