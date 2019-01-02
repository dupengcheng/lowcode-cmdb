# coding=utf-8

from flask import Flask, request, render_template, redirect, url_for, session
from config import db_config, page_config, page_config2
from dbutil.dbutil import DB
from dbutil.pageutil import PageConf
from asyncutil.asyncutil import Task
from copy import deepcopy
import json

app = Flask(__name__)
app.secret_key = 'xxx'
db = DB(mysql_db=db_config['db'])
pageutil=PageConf(db)
task = Task(4)
page_config.setdefault('favicon', '/static/img/favicon.ico')
page_config.setdefault('title', 'Woniu-cmdb')
page_config.setdefault('brand_name', 'Woniu-cmdb')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/')
    if request.method == "POST":
        name = request.form.get('username')
        passwd = request.form.get('password')
        #print(name + "  " + passwd)
        obj = {"result": 1}
        if name and passwd:
            sql = 'select * from user where username="%s" and password="%s"' % (name, passwd)
            #print(sql)
            cur = db.execute(sql)
            # #print cur.fetchone()
            if cur.fetchone():
                obj["result"] = 0
                session['username'] = name
        return json.dumps(obj)
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')


@app.route('/page/<template>')
def render(template):
    if 'username' in session:
        #print(template, page_config, page_config2)
        # sql = "select s.colume_name,s.colume_title , t.name,t.title from string_clo s inner join   table_info t on t.id = s.table_name;"
        # cur = db.execute(sql)
        # records = cur.fetchall()
        # page_conf = {}
        # for record in records:
        #     table_name = record["name"]
        #     table_title = record["title"]
        #     colume_name = record["colume_name"]
        #     colume_title = record["colume_title"]
        #     colume_dict = {"name": colume_name, "title": colume_title}
        #     page_conf[table_name] = page_conf.get(table_name, {"name": table_name,
        #                                                        "title": table_title,
        #                                                        "data": []})
        #     page_conf[table_name].get("data", []).append(colume_dict)

        page_conf=pageutil.conf_page()
        #print("----------------- ppppppppppppp",json.dumps( page_conf))
        all_page = deepcopy(page_config)
        all_page["menu"].extend(page_conf.values())
        #print("*******memconf*******", page_conf.values())
        #print("*********allconf*****", json.dumps(page_config["menu"]))
        page_json=page_config2.get(template,page_conf.get(template,{}))
        return render_template('page/common.html', data=all_page, page_json=page_json,
                               username=session['username'])
        # return render_template('page/'+template+'.html',data=page_config,username=session['username'])

    else:
        return redirect('/login')


@app.route('/addapi', methods=['POST'])
def addapi():
    obj = request.form.to_dict()
    table = obj.pop('action_type')
    keys = obj.keys()
    values = obj.values()
    #print(values)
    valuestr = map(lambda x: "?", values)

    sql = 'insert into %s (%s) values (%s)' % (table, ','.join(keys), ','.join(valuestr))
    #print(sql)
    db.execute(sql, parameters=tuple(values))
    res = {'result': 'ok'}
    return json.dumps(res)


@app.route('/delapi', methods=['POST'])
def delapi():
    obj = request.form.to_dict()
    table = obj.pop('action_type')
    table_id = obj.pop('id')
    sql = 'delete from %s where id=%s' % (table, table_id)
    # sql = 'insert into %s (%s) values ("%s")' % (table,','.join(keys),'","'.join(values))
    #print(sql)
    db.execute(sql)
    res = {'result': 'ok'}
    return json.dumps(res)


@app.route('/listapi')
def listapi():
    action_type = request.args.get('action_type')
    sql = 'select * from ' + action_type
    cur = db.execute(sql)
    res = {"result": cur.fetchall()}
    #print(json.dumps(res))
    return json.dumps(res)


@app.route('/updateapi', methods=['POST'])
def updateapi():
    obj = request.form.to_dict()
    table = obj.pop('action_type')
    table_id = obj.pop('id')
    arr = []
    params = []
    for key, val in obj.items():
        arr.append(key + '=?')
        params.append(val)
    #print("%s   %s" % (arr, params))
    keys = obj.keys()
    values = obj.values()
    sql = 'update %s set ' % (table)

    sql += ','.join(arr)
    sql += ' where id=' + table_id
    #print(sql)
    db.execute(sql, parameters=tuple(params))
    res = {'result': 'ok'}
    return json.dumps(res)


@app.before_request
def before_request():
    # 拦截所有请求
    user_id = session.get("username")
    # #print("xxxx   ", user_id, request.method)
    # #print("yyyyy  ", page_config)
    # #print("zzzzz  ", page_config2)
    # post请求拿到请求体和请求路径传递给异步处理方法
    if "POST" == request.method:
        obj = request.form.to_dict()
        for key in ["table_name", "select_table_name"]:
            if key in obj.keys():
                sql = 'select name from %s where id=%s' % ("table_info", obj[key])
                res = db.execute(sql).fetchone()
                #print("select name from table_info result ", res)
                if res and "name" in res.keys():
                    obj["_" + key] = res["name"]
        obj["_request_endpoint"] = request.endpoint
        obj["_request_db"] = db_config['db']
        task.submit(obj)
        #print("before_request", user_id, obj, request.endpoint)


@app.route('/')
def index():
    return redirect('/page/user')
    # return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=9092, host='0.0.0.0')
