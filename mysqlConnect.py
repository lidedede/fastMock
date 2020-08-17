#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by dedong on 2018/7/9
import pymysql


class MysqlConnect():
    def __init__(self, dbinfo={}):
        conn = pymysql.connect(host=dbinfo["HOST"],
                               port=3306,
                               user=dbinfo["USER"],
                               password=dbinfo["PWD"],
                               db=dbinfo["DB"],
                               charset='utf8')
        self.conn = conn

    def query(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def excute(self, sql, args):
        cursor = self.conn.cursor()
        # info = {'name': 'fake', 'age': 15}
        effect_row = cursor.execute(sql, args)
        self.conn.commit()
        return effect_row

    def __del__(self):
        self.conn.close()