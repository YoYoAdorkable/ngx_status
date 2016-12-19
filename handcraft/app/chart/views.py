# coding: utf-8
from flask import render_template, redirect, request, url_for, flash
#from flask_login import login_user, login_required, logout_user
from . import chart
from .. import db
from ..models import User
#from .forms import LoginForm, RegistrationForm, EmailForm, PasswordForm
from .. import Config
#from itsdangerous import URLSafeTimedSerializer
from flask import current_app
#from ..send_mail import *
import MySQLdb as mdb
from flask import jsonify
import datetime
import time

@chart.route('/traffic', methods=['GET'])
def traffic():
    # flow chart
    SELECT_SQL="SELECT right(Timespan,8),inbound,outbound FROM ngx_flow where ip = '192.168.200.134' and domain = 'www.yoyohandcraft.cn' ORDER BY Timespan DESC LIMIT 30"
    Result = operating_db(SELECT_SQL)
    Times = []
    Inbounds = []
    Outbounds = []
    for i in Result:
        Times.append(list(i)[0])
        Inbounds.append(list(i)[1])
        Outbounds.append(list(i)[2])
    
    Timespan = list(reversed(Times))
    Inbound = list(reversed(Inbounds))
    Outbound = list(reversed(Outbounds))
    
    flow_dict = {}
    keys=[Timespan,Inbound,Outbound]
    key=['Timespan','Inbound','Outbound']
    for k in key:
        flow_dict[k] = keys[key.index(k)]
   
    # code chart
    SELECT_SQL="SELECT right(Timespan,8),2xx,3xx,4xx,5xx FROM ngx_status_code where ip = '192.168.200.134' and domain = 'www.yoyohandcraft.cn' ORDER BY Timespan DESC LIMIT 15"
    Result = operating_db(SELECT_SQL)
    Times = []
    xx2 = []
    xx3 = []
    xx4 = []
    xx5 = []
    for i in Result:
        Times.append(list(i)[0])
        xx2.append(list(i)[1])
        xx3.append(list(i)[2])
        xx4.append(list(i)[3])
        xx5.append(list(i)[4])

    Timespan = list(reversed(Times))
    XX2 = list(reversed(xx2))
    XX3 = list(reversed(xx3))
    XX4 = list(reversed(xx4))
    XX5 = list(reversed(xx5))

    code_dict = {}
    keys=[Timespan,XX2,XX3,XX4,XX5]
    key=['Timespan','XX2','XX3','XX4','XX5']
    for k in key:
        code_dict[k] = keys[key.index(k)]
 
    # main
    r_dict = {}
    r_dict['flow'] = flow_dict
    r_dict['code'] = code_dict
    return jsonify(r_dict)

@chart.route('/summary', methods=['GET'])
def summary():
    SELECT_INFO_SQL="SELECT * from ngx_info where ip = '192.168.200.134' ORDER BY id DESC LIMIT 1;"
    Result_INFO=operating_db_dict(SELECT_INFO_SQL)
    nginx_version = []
    nginx_ip = []
    nginx_pid = []
    nginx_uptime = []
    nginx_total = []
    nginx_active = []
    nginx_reading = []
    nginx_writing = []
    nginx_waiting = []
    nginx_current = []

    if Result_INFO:
        nginx_version.append(Result_INFO[0]['version'])
        nginx_ip.append(Result_INFO[0]['ip'])
        nginx_pid.append(Result_INFO[0]['pid'])
        nginx_uptime.append(uptime(Result_INFO[0]['start_time']))
    else:
        nginx_version.append(0)
        nginx_ip.append(0)
        nginx_pid.append(0)
        nginx_uptime.append(0)

    SELECT_CONN_SQL="SELECT * from ngx_connections where ip = '192.168.200.134' ORDER BY id DESC LIMIT 1;"
    Result_CONN=operating_db_dict(SELECT_CONN_SQL)
    if Result_CONN:
        nginx_total.append(Result_CONN[0]['total'])
        nginx_active.append(Result_CONN[0]['active'])
        nginx_reading.append(Result_CONN[0]['reading'])
        nginx_writing.append(Result_CONN[0]['writing'])
        nginx_waiting.append(Result_CONN[0]['waiting'])
        nginx_current.append(Result_CONN[0]['current'])
    else:
        nginx_total.append(0)
        nginx_active.append(0)
        nginx_reading.append(0)
        nginx_writing.append(0)
        nginx_waiting.append(0)
        nginx_current.append(0)

    info_dict = {}
    keys=[nginx_version,nginx_ip,nginx_pid,nginx_uptime,nginx_total,nginx_active,nginx_reading,nginx_writing,nginx_waiting,nginx_current]
    key=['nginx_version','nginx_ip','nginx_pid','nginx_uptime','nginx_total','nginx_active','nginx_reading','nginx_writing','nginx_waiting','nginx_current']
    for k in key:
        info_dict[k] = keys[key.index(k)]

    return jsonify(info_dict)


def uptime(result):
    today_now=datetime.datetime.now()
    today = time.mktime(today_now.timetuple)
    start_time=datetime.datetime.strptime(result, '%Y-%m-%d %H:%M:%S')
    start = time.mktime(start_time.timetuple)
    Difference= int(today - start)
    ss = 60
    hh = ss * 60
    dd = hh * 24
    day= Difference / dd
    hour = (Difference - day * dd) / hh
    minute = (Difference - day * dd - hour * hh) / ss
    result=str(day)+'d '+str(hour)+'h '+str(minute)+'m'

    return result

def operating_db ( sql = '' ):
    db_host = current_app.config['MYSQL_HOST']
    db_user = current_app.config['MYSQL_USER']
    db_pass = current_app.config['MYSQL_PASS']
    db_name = current_app.config['MYSQL_NGX_DB']

    con = mdb.connect(db_host, db_user, db_pass, db_name , charset="utf8")

    try:
        with con:
            cur = con.cursor()
            cur.execute (sql)
            rows = cur.fetchall()
            if rows:
                return rows
            else:
                return None
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    if con_db:
        con_db.close()

def operating_db_dict ( sql = '' ):
    db_host = current_app.config['MYSQL_HOST']
    db_user = current_app.config['MYSQL_USER']
    db_pass = current_app.config['MYSQL_PASS']
    db_name = current_app.config['MYSQL_NGX_DB']

    con = mdb.connect(db_host, db_user, db_pass, db_name , charset="utf8")

    try:
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute (sql)
            rows = cur.fetchall()
            if rows:
                return rows
            else:
                return None
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    if con_db:
        con_db.close()
