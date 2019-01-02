#!/usr/bin/env python
# encoding:utf8

from concurrent.futures import ThreadPoolExecutor
from config import update_page_config2, page_config, page_config2
from dbutil.dbutil import DB


class Task:
    '''
    暂时只是完成了新增页面，没有更新逻辑，也没有删除逻辑
    demo调研基本完成
    '''
    pool = None

    def __init__(self, pool_size):
        self.pool_size = pool_size
        self.pool = ThreadPoolExecutor(pool_size)

    def submit(self, obj):
        print("task submit", obj)
        self.pool.submit(self.api_execute, obj)

    def api_execute(self, obj):
        '''
        api 入口处的增删改查操作
        对应的异步事件
        按照不同的数据库表
        在此执行不同的逻辑
        :return:
        '''
        table_name = obj.pop('action_type')
        endpoint = obj.pop('_request_endpoint')
        print("异步处理", obj)
        func_name = endpoint + "_" + table_name
        if hasattr(self, func_name):
            table_func = getattr(self, func_name)
            table_func(obj)

    # 添加一张空表
    def addapi_table_info(self, obj):
        #  表名处理
        print("start execute create table", obj)
        table_name = obj.pop("name")
        db_name = obj.pop("_request_db")
        db = DB(mysql_db=db_name)
        create_table = 'create table %s (id INTEGER PRIMARY KEY )' % table_name
        print("execute create table",create_table)
        db.execute(create_table)

    # 删除表
    def delapi_table_info(self, obj):
        table_name = obj.get("table_name", "")

    # 更新表名
    def updateapi_table_info(self, obj):
        table_id = obj["id"]
        table_name = obj.pop("name")
        db_name = obj.pop("_request_db")
        db = DB(mysql_db=db_name)
        create_table = 'alter table %s rename to ' % table_name
        print("execute create table", create_table)
        db.execute(create_table)

    def addapi_string_clo(self, obj):
        # 字符串类型 增加表字段
        print("string_clo", obj)
        # string_clo {'colume_name': 'col1', 'colume_title': '字段1', 'table_name': '3', '_table_name': 'cdcad', '_request_db': <dbutil.dbutil.DB object at 0x7f1d4df73be0>}
        table_name = obj.pop("_table_name")
        db_name = obj.pop("_request_db")
        db = DB(mysql_db=db_name)
        colume_name = obj.get("colume_name", "")
        # create_table = 'create table %s (id INTEGER PRIMARY KEY )' % table_name
        add_colume = "ALTER TABLE %s ADD COLUMN %s varchar(200) " % (table_name, colume_name)
        # db.execute(create_table)
        db.execute(add_colume)

    def delapi_string_clo(self, obj):
        # 字符串类型 表字段修改处理
        print("string_clo", obj)

    def updateapi_string_clo(self, obj):
        # 字符串类型 表字段修改处理
        print("string_clo", obj)

    # -------------------------------

    # endpoint = obj.pop('_request_endpoint')
    # if endpoint == "addapi":
    #     pass
    # if endpoint == "delapi":
    #     pass
    # if endpoint == "updateapi":
    #     pass
    def addapi_datetime_clo(self, obj):
        # 日期类型 表字段修改处理
        print("datetime_clo", obj)
        table_name = obj.pop("_table_name")
        db_name = obj.pop("_request_db")
        db = DB(mysql_db=db_name)
        colume_name = obj.get("colume_name", "")
        # create_table = 'create table %s (id INTEGER PRIMARY KEY )' % table_name
        add_colume = "ALTER TABLE %s ADD COLUMN %s varchar(200) " % (table_name, colume_name)
        # db.execute(create_table)
        db.execute(add_colume)

    def addapi_dynamic_select_clo(self, obj):
        # 动态选择类型 表字段修改处理
        print("dynamic_select_clo", obj)
        table_name = obj.pop("_table_name")
        db_name = obj.pop("_request_db")
        db = DB(mysql_db=db_name)
        colume_name = obj.get("colume_name", "")
        # create_table = 'create table %s (id INTEGER PRIMARY KEY )' % table_name
        add_colume = "ALTER TABLE %s ADD COLUMN %s varchar(200) " % (table_name, colume_name)
        # db.execute(create_table)
        db.execute(add_colume)

    def addapi_static_select_clo(self, obj):
        # 静态选择类型 表字段修改处理
        print("static_select_clo", obj)
        table_name = obj.pop("_table_name")
        db_name = obj.pop("_request_db")
        db = DB(mysql_db=db_name)
        colume_name = obj.get("colume_name", "")
        # create_table = 'create table %s (id INTEGER PRIMARY KEY )' % table_name
        add_colume = "ALTER TABLE %s ADD COLUMN %s varchar(200) " % (table_name, colume_name)
        # db.execute(create_table)
        db.execute(add_colume)
