# _*_ coding: utf-8 _*_

"""
pro_save.py by shai
"""
import sys
import pymysql

class Saver(object):
    """
    class of Saver, must include function working(), file_save() and db_insert()
    """

    def __init__(self, save_type, file_name=None, db_info=None):
        """
        constructor
        """
        if save_type == "file" and file_name:
            self.file_name = file_name
            self.save_pipe = open(file_name, "w", encoding="utf-8")
        elif save_type == "db":
            self.db_info = db_info
            self.conn = pymysql.connect(host=db_info.get("host"), user=db_info.get("user"),
                                        passwd=db_info.get("passwd"), db=db_info.get("db"),
                                        charset=db_info.get("charset"))
            #self.conn = pymysql.connect(host='127.0.0.1', user='shai', passwd='Thermo2014!', db='SHREPA', charset='utf8')
        else:
            sys.stdout
    def db_prep(self, dataset):
        pass

    def db_insert(self, sql, dataset):
        cur = self.conn.cursor()
        cur.execute(sql, dataset)
        cur.connection.commit