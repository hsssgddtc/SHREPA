# _*_ coding: utf-8 _*_

import re
import urllib2


a=u"新加坡怡安物业管理有限公司、狮城怡安(上海)物业管理有限公司、大华集团上海浦华物业管理有限公司                                                                                                                                                                                                                                            新加坡怡安物业管理有限公司狮城怡安(上海)物业管理有限公司大华集团上海浦华物业管理有限公司\
\
\
\
\
\
sdfasdf"

#print(a.replace(" ",""))

#print(len(a.replace(" ","")))



#temp = re.search(r"(?P<num>\d+(\.\d+)?)(?P<param>[\w\W]*?)$", string.upper().strip(), flags=re.IGNORECASE)

#print(temp.group("num"))
#print(temp.group("param"))





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
    get string striped \t, \r, \n from a string, also change None to ""
    """
    return re.sub(r"\s+", " ", string, flags=re.IGNORECASE).strip() if string else ""


def get_url_legal(url, base_url, encoding=None):
    """

    :param url: 
    :param base_url: 
    :param encoding: 
    :return: 
    """
    url_join = urllib2.urljoin(base_url, url, allow_fragments=True)
    url_legal = urllib2.quote(url_join, safe="%/:=&?~#+!$,;'@()*[]|", encoding=encoding)
    url_frags = urllib2.urlparse(url_legal, allow_fragments=True)
    return urllib2.parse.urlunparse(
        (url_frags.scheme, url_frags.netloc, url_frags.path, url_frags.params, url_frags.query, ""))


item_list = [<span class="item-cell item-label">\u6700\u4f4e\u9996\u4ed8</span>, <span class="item-cell">185.5\u4e07</span>,
<span class="item-cell item-label">\u53c2\u8003\u6708\u4f9b</span>,
<span class="item-cell">18284\u5143</span>,
<span class="item-cell item-label">\u5c0f\u533a\u540d\u79f0</span>,
<span class="item-cell">\n<span class="maininfo-estate-name"><a class="u-link" gahref="ershoufang_gaiyao_xiaoqu_link" href="/xiaoqu/5017953113780379.html" target="_blank" title="\u4fdd\u5229\u53f6\u4e0a\u6d77\uff08\u4e00\u671f\uff09">\u4fdd\u5229\u53f6\u4e0a\u6d77\uff08\u4e00\u671f\uff09</a>\xa0(<a class="u-link" href="/ershoufang/baoshan" target="_blank">\u5b9d\u5c71</a>\xa0<a class="u-link" href="/ershoufang/gucun" target="_blank">\u987e\u6751</a>)</span>\xa0\xa0\xa0<a class="u-link u-mt8" href="javascript:;" id="jumpToAround">\u5730\u56fe</a>\n</span>,
<span class="item-cell item-label">\u6240\u5728\u5730\u5740</span>,
<span class="item-cell maininfo-estate-address" title="\u83ca\u592a\u8def1198\u5f04">\u83ca\u592a\u8def1198\u5f04</span>, <span class="item-cell item-label">\u770b\u623f\u65f6\u95f4</span>, <span class="item-cell">\u968f\u65f6\u770b\u623f</span>,
<span class="item-cell item-label">\u623f\u6e90\u7f16\u53f7</span>,
<span class="item-cell">\n                            sh4577926\n                            \n                                <a class="u-link u-ml20" gahref="ershoufang_xujia" href="javascript:;" id="btn_report">\u4e3e\u62a5</a>\n<a class="u-link u-ml16" href="http://www.lianjia.com/zhuanti/pfgz" target="blank">\u5047\u4e00\u8d54\u767e\u7ec6\u5219</a>\n</span>]


#BASE_URL = "http://sh.lianjia.com"
#URL = "/ershoufang/sh2313123.html"
#print(get_url_legal(URL, BASE_URL))

#print(a)
#print(get_string_strip(a))

#print(hash("dfsasfdasfasfasds"))