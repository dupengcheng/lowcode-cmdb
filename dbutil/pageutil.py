#!/usr/bin/env python
# encoding:utf8
import time
import json
import sqlite3
from config import page_config2


class PageConf:
    db = None

    def __init__(self, db):
        self.db = db

    def conf_page(self):
        page_conf = {}

        page_conf = self.string_col(page_conf)
        page_conf = self.datetime_clo(page_conf)
        page_conf = self.dynamic_select_clo(page_conf)
        page_conf = self.static_select_clo(page_conf)
        # print("PageConf.conf_page ", page_conf)
        return page_conf

    def string_col(self, page_conf):
        sql = "select s.colume_name,s.colume_title , t.name,t.title from string_clo s inner join   table_info t on t.id = s.table_name;"
        cur = self.db.execute(sql)
        records = cur.fetchall()
        for record in records:
            table_name = record["name"]
            table_title = record["title"]
            colume_name = record["colume_name"]
            colume_title = record["colume_title"]
            colume_dict = {"name": colume_name, "title": colume_title}
            page_conf[table_name] = page_conf.get(table_name, {"name": table_name,
                                                               "title": table_title,
                                                               "data": []})
            page_conf[table_name].get("data", []).append(colume_dict)
        return page_conf

    def datetime_clo(self, page_conf):
        sql = "select s.colume_name,s.colume_title , t.name,t.title from datetime_clo s inner join   table_info t on t.id = s.table_name;"
        cur = self.db.execute(sql)
        records = cur.fetchall()
        for record in records:
            table_name = record["name"]
            table_title = record["title"]
            colume_name = record["colume_name"]
            colume_title = record["colume_title"]
            colume_dict = {"name": colume_name, "title": colume_title, "type": 'date'}
            page_conf[table_name] = page_conf.get(table_name, {"name": table_name,
                                                               "title": table_title,
                                                               "data": []})
            page_conf[table_name].get("data", []).append(colume_dict)
        return page_conf

    def dynamic_select_clo(self, page_conf):
        sql = "select s.colume_name,s.colume_title,a.name select_table_name,t.name ,t.title " \
              "from dynamic_select_clo s " \
              "inner join   table_info t on t.id = s.table_name " \
              "inner join   table_info a on a.id = s.select_table_name;"
        cur = self.db.execute(sql)
        records = cur.fetchall()
        for record in records:
            table_name = record["name"]
            table_title = record["title"]
            colume_name = record["colume_name"]
            colume_title = record["colume_title"]
            select_table_name = record["select_table_name"]
            colume_dict = {"name": colume_name, "title": colume_title, "type": 'select',
                           "select_type": select_table_name}
            page_conf[table_name] = page_conf.get(table_name, {"name": table_name,
                                                               "title": table_title,
                                                               "data": []})
            page_conf[table_name].get("data", []).append(colume_dict)
        return page_conf

    def static_select_clo(self, page_conf):
        sql = "select s.colume_name,s.colume_title ,s.select_value , t.name,t.title from static_select_clo s " \
              "inner join   table_info t on t.id = s.table_name;"
        cur = self.db.execute(sql)
        records = cur.fetchall()
        for record in records:
            table_name = record["name"]
            table_title = record["title"]
            colume_name = record["colume_name"]
            colume_title = record["colume_title"]
            select_value = record["select_value"]
            select_value = json.loads(select_value)
            colume_dict = {"name": colume_name, "title": colume_title, "type": 'select', "value": select_value}
            page_conf[table_name] = page_conf.get(table_name, {"name": table_name,
                                                               "title": table_title,
                                                               "data": []})
            page_conf[table_name].get("data", []).append(colume_dict)
            # print("PageConf.static_select_clo", colume_dict)
        return page_conf
