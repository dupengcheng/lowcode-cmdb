# coding=utf-8


# 数据库配置


db_config = {
    'db': 'cmdb'
}

page_config = {
    "brand_name": '51Reboot',
    'title': 'hello reboot',
    "favicon": 'https://pic1.zhimg.com/6d660dd4156c64bfad13ff97d79c2f98_l.jpg',
    "menu": [
        {
            # user配置最好不要修改，是和登陆认证相关的，直接在下面加配置即可
            "name": 'user',
            "title": '用户管理',
            "data": [{
                "name": 'username',
                "title": '用户名'
            }, {
                "name": 'password',
                "title": '密码'
            }]
        },

        {
            "name": 'table_info',
            "title": '系统设置',
            "data": [{
                "name": "name",
                "title": '数据表英文名'
            },{
                "name": "title",
                "title": '数据表中文名'
            }]
        },


        {
            "title": '更多设置',
            "sub": [
                {
                    'name': 'string_clo',
                    'title': '字符串',
                    'data': [{
                        'name': 'colume_name',
                        'title': '字段英文名'
                    }, {
                        'name': 'colume_title',
                        'title': '字段中文名'
                    }, {
                        'name': 'table_name',
                        'title': '表名',
                        "type": 'select',
                        "select_type": 'table_info'
                    }]
                },
                {
                    'name': 'datetime_clo',
                    'title': '日期',
                    'data': [{
                        'name': 'colume_name',
                        'title': '字段英文名'
                    }, {
                        'name': 'colume_title',
                        'title': '字段中文名'
                    }, {
                        'name': 'table_name',
                        'title': '表名',
                        "type": 'select',
                        "select_type": 'table_info'
                    }]
                },

                {
                    'name': 'dynamic_select_clo',
                    'title': '动态选择器',
                    'data': [{
                        'name': 'colume_name',
                        'title': '字段英文名'
                    }, {
                        'name': 'colume_title',
                        'title': '字段中文名'
                    }, {
                        'name': 'table_name',
                        'title': '表名',
                        "type": 'select',
                        "select_type": 'table_info'
                    }, {
                        'name': 'select_table_name',
                        'title': '被选表名',
                        "type": 'select',
                        "select_type": 'table_info'
                    }]
                },
                {
                    'name': 'static_select_clo',
                    'title': '静态选择器',
                    'data': [{
                        'name': 'colume_name',
                        'title': '字段英文名'
                    }, {
                        'name': 'colume_title',
                        'title': '字段中文名'
                    }, {
                        'name': 'table_name',
                        'title': '表名',
                        "type": 'select',
                        "select_type": 'table_info'
                    }, {
                        'name': 'select_value',
                        'title': '配置格式  {0: "开启", 1: "关闭"}',
                    }]
                }

            ]
        }
    ]
}
page_config2 = {}
def update_page_config2():
    for page in page_config["menu"]:
        if "name" in page.keys():
            name = page["name"]
            page_config2[name] = page
        if "sub" in page.keys():
            for sub in page["sub"]:
                name = sub["name"]
                page_config2[name] = sub

update_page_config2()






# '''
# page_config2_demo = {
#     "brand_name": '51Reboot',
#     'title': 'hello reboot',
#     "favicon": 'https://pic1.zhimg.com/6d660dd4156c64bfad13ff97d79c2f98_l.jpg',
#     "menu": {
#         'user': {
#             # user配置最好不要修改，是和登陆认证相关的，直接在下面加配置即可
#             "name": 'user',
#             "title": '用户管理',
#             "data": [{
#                 "name": 'username',
#                 "title": '用户名'
#             }, {
#                 "name": 'password',
#                 "title": '密码'
#             }]
#         },
#         'test': {
#             # user配置最好不要修改，是和登陆认证相关的，直接在下面加配置即可
#             "name": 'test',
#             "title": '测试',
#             "data": [{
#                 "name": 'username',
#                 "title": '用户名'
#             }, {
#                 "name": 'password',
#                 "title": '密码',
#                 "empty": "yes"
#
#             }]
#         },
#         'caninet': {
#             "name": 'caninet',
#             "title": '机柜',
#             "data": [{
#                 "name": "name",
#                 "title": '机柜名'
#             }]
#         },
#         "host": {
#             "name": "host",
#             "title": "服务器",
#             "data": [{
#                 "name": "caninet",
#                 "title": '机柜',
#                 "type": 'select',
#                 "select_type": 'caninet'
#             }, {
#                 "name": "hostname",
#                 "title": '主机名'
#             }, {
#                 'name': 'asset_no',
#                 'title': '资产号'
#             }, {
#                 "name": 'end_time',
#                 "title": "过期日期",
#                 "type": 'date'
#             }, {
#                 "name": 'ups',
#                 "title": '是否开启',
#                 "type": 'select',
#                 "value": {0: '开启', 1: '关闭'}
#             }]
#     }
#     }
# }
# '''

# ,{
#         "name": 'host',
#         "title": '服务器',
#         "data": [{
#             "name": 'cabinet',
#             "title": '机柜'
#         },{
#             "name":'hostname',
#             "title":'主机名'
#         }]
#     },{
#         "title": '业务',
#         "sub":[
#             {
#                 'name': 'product',
#                 'title': '业务线',
#                 'data': [{
#                     'name': 'service_name',
#                     'title': '服务名'
#                 },{
#                     'name':'module_letter',
#                     'title':'模块简称'
#                 },{
#                     'name':'dev_interface',
#                     'title':'开发者'
#                 },{
#                     'name':'op_interface',
#                     'title':'运维接口人'
#                 }]
#             },
#             {
#                 'name': 'raidtype',
#                 'title': 'Raid厂商',
#                 'data': [{
#                     'name': 'name',
#                     'title': 'Raid厂商'
#                 }]
#             }


#         ]
#     }
