# _*_ coding: utf-8 _*_

"""
pro_parse.py by shai
"""

class Parser(object):
    """
    class of Parser, must include working and html_parse()
    """

    def __init__(self, max_deep=0, max_repeat=0):
        """
        constructor
        """
        self.max_deep = max_deep    # default: 0, if -1, spider will not stop until all urls are fetched
        self.max_repeat = max_repeat    #default: 0 maximum repeat time for parsing content

        self.log_str_format = "url=%s, priority=%s, keys=%s, deep=%s, critical=%s, parse_repeat=%s"
        return

    def html_parse(self, content):
        """
        parse the content of a url, this function can be rewrite, parameters and return refer to self.working()
        """
        url_list = []
        content_dict = {}
        cur_code, cur_url, cur_html = content

        return 1, url_list, content_dict