#!/usr/bin/env python
# encoding:utf8
import time
import sqlite3
from config import page_config2


class DB:
    conn = None

    def __init__(self, mysql_db):
        self.mysql_db = mysql_db

    def connect(self):
        print("conn start" + self.mysql_db)
        self.conn = sqlite3.connect(self.mysql_db)
        print("conn end" + self.mysql_db)

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def execute(self, sql, **parameters):
        try:
            parameters = parameters.get("parameters") if parameters.get("parameters") else ()
            print(sql)
            print("parameters is ", parameters)
            self.conn = sqlite3.connect(self.mysql_db, isolation_level=None)
            self.conn.row_factory = self.dict_factory
            cursor = self.conn.cursor()
            self.conn.cursor()
            cursor.execute(sql, parameters)
            # cursor.close()
            # self.conn.commit()
            # self.conn.close()
        except sqlite3.Error as e:
            err_msg = e.args[0]
            print("An error occurred:", e.args[0])
            if "no such table" in err_msg:
                table = err_msg.split(":")[1].strip()
                print("create table ", table)
                self.create_table(table)
                # page_config2[template]
            try:
                cursor.close()
                self.conn.close()
            except:
                pass
            time.sleep(1)
            try:
                self.connect()
                print("reconnect DB")
                cursor = self.conn.cursor()
                cursor.execute(sql)
            except sqlite3.Error as e:
                print("An error occurred:", e.args[0])
                time.sleep(2)
                self.connect()
                print("reconnect DB")
                cursor = self.conn.cursor()
                cursor.execute(sql)

        return cursor

    def create_table(self, name):
        if name not in page_config2.keys():
            return
        if "data" not in page_config2[name]:
            return
        data = page_config2[name]["data"]
        tmp = []
        for v in data:
            tmp.append('%s varchar(200)' % v['name'])
        sql = 'create table %s (id INTEGER PRIMARY KEY ,%s)' % (name, ','.join(tmp))
        print(sql)
        self.execute(sql)
        print('table %s is created' % name)
        if "user" == name:
            self.execute('insert into user (username,password) values ("admin","admin")')

