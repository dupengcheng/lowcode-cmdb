#!/usr/bin/env python
# encoding:utf8
import json
import time, random
import datetime
import sqlite3


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
            print("An error occurred:", e.args[0])
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
