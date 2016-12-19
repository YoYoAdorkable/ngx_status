#!/usr/bin/python
#coding:utf-8

import os,sys
import urllib2
import logging
import requests
import json
import time
import datetime
import MySQLdb as mdb
from multiprocessing.pool import ThreadPool
from apscheduler.schedulers.blocking import BlockingScheduler

####################################################################################################################
#	Current_time：当前时间	   Ip：IP地址	  Url：访问地址      Result：请求结果	  Data：json格式化数据	       #
#	Keys：json数据第一层key    Master_key：第二层key      Deputy_key：第三层key	Final_key：最后一层key	           #
####################################################################################################################

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] \
                    %(levelname)s %(message)s',
                    filename='/tmp/nginx_status.log',
                    filemode='a'
                    )

def operating_db ( sql = '' ):
    db_user = 'ngx_status'
    db_password = 'ngx_status'
    db_hostname = '192.168.200.125'
    db_name = 'ngx_status'

    con = mdb.connect(db_hostname, db_user, db_password , db_name , charset="utf8")

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

#def replace_dot(obj):
#    for key in obj.keys():
#        new_key = key.replace(".","_")
#        if new_key != key:
#            obj[new_key] = obj[key]
#            del obj[key]
#    return obj

def request_ngx(host):
    r_dict = {host: []}
    for i in range(1):
        try:
            r = requests.get('http://%s/status' % host, timeout=3)
        except Exception as e:
            logging.exception(e)
            continue
        if r.status_code != 200:
            print '无法访问'
        r_dict[host].append(r.json(parse_int=int))
        #r_dict[host].append(r.json(parse_int=int, object_hook=replace_dot))
        #r_dict[host].append(r.json(parse_int=float, object_hook=replace_dot))
    return None if all(x is None for x in r_dict[host]) else r_dict

 
def Analysis_keys(Result):
    Timespan=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for r_dict in Result:
        if r_dict:
            for k in r_dict:
                Data=r_dict.values()[0][0]
                Time_keys=Data['global'].keys()
                Keys=Data.keys()
                if 'conn_time' in Time_keys:
                    start_time=Data['global']['start_time']
                    conn_time=Data['global']['conn_time']
                    Query_SQL="select * from ngx_connections where conn_time = '%s' limit 1" %(conn_time)
                    Results=operating_db(Query_SQL)
                    if not Results: 
                        for num in range(len(Keys)):
                            Key=Keys[num]
                            Master_key=Data[Key].keys()
                            if ':' in k:
                                Ip=k.split(':')[0]
                            else:    
                                Ip=k
                            Analytical_results(Ip,Data,Key,Master_key,Timespan,conn_time,start_time)
                    else:
                        print '数据未更新'
                        Keys.remove('global')
                        for num in range(len(Keys)):
                            Domain=Keys[num]
                            if ':' in k:
                                Ip=k.split(':')[0]
                            else:
                                Ip=k
                            
                            Default_data_storage(Ip,Domain,Timespan,conn_time,start_time)
                else:
                    print '没有访问'

def Analytical_results(Ip,Data,Key,Master_key,Timespan,conn_time,start_time):
    if Key == 'global':
        active=Data[Key]['connections']['active']
    	reading=Data[Key]['connections']['reading']
    	writing=Data[Key]['connections']['writing']
    	waiting=Data[Key]['connections']['waiting']
    	total=Data[Key]['requests']['total']
    	current=Data[Key]['requests']['current']
    	pid=Data[Key]['PID']
    	version=Data[Key]['Version']
       
        Select_SQL="select sum(total) as total from ngx_connections where ip = '%s' and start_time = '%s';" %(Ip,start_time)
        requests_total_Data_Library=operating_db(Select_SQL)
        if requests_total_Data_Library[0]['total'] is not None:
            total=total-int(requests_total_Data_Library[0]['total'])
	    
        Insert_SQL="insert into ngx_connections(ip,Timespan,active,reading,writing,waiting,total,current,conn_time,start_time) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" %(Ip,Timespan,active,reading,writing,waiting,total,current,conn_time,start_time)
        operating_db(Insert_SQL)

        Replace_SQL ="replace into ngx_info(ip,pid,version,start_time) values('%s','%s','%s','%s');" %(Ip,pid,version,start_time)
        operating_db(Replace_SQL)

    else:
        Domain=Key
        Deputy_key=Data[Key].keys()
        if 'upstream_requests_total' in Deputy_key:
            upstream_requests_total=Data[Key]['upstream_requests_total']
            Deputy_key.remove('upstream_requests_total')
        else:
            upstream_requests_total=0
        if 'upstream_resp_time_sum' in Deputy_key:	
            upstream_resp_time_sum=Data[Key]['upstream_resp_time_sum']
            Deputy_key.remove('upstream_resp_time_sum')
        else:
            upstream_resp_time_sum=0
        
        requests_total=Data[Key]['requests_total']
        Inbound=Data[Key]['traffic']['received']
        Outbound=Data[Key]['traffic']['sent']

        Select_SQL="SELECT sum(inbound) as inbound,sum(outbound) as outbound,sum(requests_total) as requests_total from ngx_flow where domain = '%s' and ip = '%s' and start_time = '%s';" %(Domain,Ip,start_time)
        bound_Data_Library=operating_db(Select_SQL)
        if bound_Data_Library:
            if bound_Data_Library[0]['inbound'] is not None:
                Inbound=Inbound-int(bound_Data_Library[0]['inbound'])
            if bound_Data_Library[0]['outbound'] is not None:
                Outbound=Outbound-int(bound_Data_Library[0]['outbound'])
            if bound_Data_Library[0]['requests_total'] is not None:
                requests_total=requests_total-int(bound_Data_Library[0]['requests_total'])

        Insert_SQL="insert into ngx_flow(domain,Timespan,inbound,outbound,requests_total,ip,start_time) values('%s','%s','%s','%s','%s','%s','%s');" %(Domain,Timespan,Inbound,Outbound,requests_total,Ip,start_time)
        operating_db(Insert_SQL) 
        Deputy_key.remove('requests_total')
        Deputy_key.remove('traffic')

        for num in range(len(Deputy_key)):
            Keyword = Deputy_key[num]
            if Keyword == 'status code':
                Final_key=Data[Key][Keyword].keys()
                if '2xx' in Final_key:
                    xx2=Data[Key][Keyword]['2xx']
                else:
                    xx2=0
                if '3xx' in Final_key:
                    xx3=Data[Key][Keyword]['3xx']
                else:
                    xx3=0
                if '4xx' in Final_key:
                    xx4=Data[Key][Keyword]['4xx']
                else:
                    xx4=0
                if '5xx' in Final_key:
                    xx5=Data[Key][Keyword]['5xx']
                else:
                    xx5=0
                Select_SQL="SELECT sum(2xx) as 2xx,sum(3xx) as 3xx,sum(4xx) as 4xx,sum(5xx) as 5xx from ngx_status_code where domain = '%s' and ip = '%s' and start_time = '%s';" %(Domain,Ip,start_time)
                status_code_Data_Library=operating_db(Select_SQL)
                if status_code_Data_Library:
                    if status_code_Data_Library[0]['2xx'] is not None:
                        xx2=xx2-int(status_code_Data_Library[0]['2xx'])
                    if status_code_Data_Library[0]['2xx'] is not None:
                        xx3=xx3-int(status_code_Data_Library[0]['3xx'])
                    if status_code_Data_Library[0]['2xx'] is not None:
                        xx4=xx4-int(status_code_Data_Library[0]['4xx'])
                    if status_code_Data_Library[0]['2xx'] is not None:
                        xx5=xx5-int(status_code_Data_Library[0]['5xx'])
                Insert_SQL="insert into ngx_status_code(domain,Timespan,2xx,3xx,4xx,5xx,ip,start_time) values('%s','%s','%s','%s','%s','%s','%s','%s');" %(Domain,Timespan,xx2,xx3,xx4,xx5,Ip,start_time)
                operating_db(Insert_SQL) 
            elif Keyword == 'request_times':
                Final_key=Data[Key][Keyword].keys()
                if '0-100' in Final_key:
                    t0=Data[Key][Keyword]['0-100']
                else:
                    t0=0
                if '100-500' in Final_key:
                    t1=Data[Key][Keyword]['100-500']
                else:
                    t1=0
                if '500-1000' in Final_key:
                    t2=Data[Key][Keyword]['500-1000']
                else:
                    t2=0
                if '1000-inf' in Final_key:
                    t3=Data[Key][Keyword]['1000-inf']
                else:
                    t3=0
                Select_SQL="SELECT sum(t0) as t0,sum(t1) as t1,sum(t2) as t2,sum(t3) as t3 from ngx_request_times where domain='%s' and ip = '%s' and start_time = '%s';" %(Domain,Ip,start_time)
                request_times_Data_Library=operating_db(Select_SQL)
                if request_times_Data_Library:
                    if request_times_Data_Library[0]['t0'] is not None:
                        t0=t0-int(request_times_Data_Library[0]['t0'])
                    if request_times_Data_Library[0]['t1'] is not None:
                        t1=t1-int(request_times_Data_Library[0]['t1'])
                    if request_times_Data_Library[0]['t2'] is not None:
                        t2=t2-int(request_times_Data_Library[0]['t2'])
                    if request_times_Data_Library[0]['t3'] is not None:
                        t3=t3-int(request_times_Data_Library[0]['t3'])
                Insert_SQL="insert into ngx_request_times(domain,Timespan,t0,t1,t2,t3,ip,start_time) values('%s','%s','%s','%s','%s','%s','%s','%s');" %(Domain,Timespan,t0,t1,t2,t3,Ip,start_time)
                operating_db(Insert_SQL) 

            elif Keyword == 'cache':
                Final_key=Data[Key][Keyword].keys()
                if 'miss' in Final_key:
                    miss=Data[Key][Keyword]['miss']
                else:
                    miss=0
                if 'hit' in Final_key:
                    hit=Data[Key][Keyword]['hit']
                else:
                    hit=0
               
            else:
                if 'cache' in Data[Key][Keyword].keys():
                    if 'miss' in Data[Key][Keyword]['cache']:
                        miss=Data[Key][Keyword]['cache']['miss']
                    else:
                        miss=0
                    if 'hit' in Data[Key][Keyword]['cache']:
                        hit=Data[Key][Keyword]['cache']['hit']
                    else:
                        hit=0
                    if 'expired' in Data[Key][Keyword]['cache']:
                        expired=Data[Key][Keyword]['cache']['expired']
                    else:
                        expired=0

                if '0-100' in Data[Key][Keyword]['request_times']:
                    t0=Data[Key][Keyword]['request_times']['0-100']
                else:
                    t0=0
                if '100-500' in Data[Key][Keyword]['request_times']:
                    t1=Data[Key][Keyword]['request_times']['100-500']
                else:
                    t1=0
                if '500-1000' in Data[Key][Keyword]['request_times']:
                    t2=Data[Key][Keyword]['request_times']['500-1000']
                else:
                    t2=0
                if '1000-inf' in Data[Key][Keyword]['request_times']:
                    t3=Data[Key][Keyword]['request_times']['1000-inf']
                else:
                    t3=0

                if '2xx' in Data[Key][Keyword]['status code']:
                    xx2=Data[Key][Keyword]['status code']['2xx']
                else:
                    xx2=0
                if '3xx' in Data[Key][Keyword]['status code']:
                    xx3=Data[Key][Keyword]['status code']['3xx']
                else:
                    xx3=0
                if '4xx' in Data[Key][Keyword]['status code']:
                    xx4=Data[Key][Keyword]['status code']['4xx']
                else:
                    xx4=0
                if '5xx' in Data[Key][Keyword]['status code']:
                    xx5=Data[Key][Keyword]['status code']['5xx']
                else:
                    xx5=0
                Keyword_requests_total=Data[Key][Keyword]['requests_total']
                error_rate=float('%0.3f' %((xx4+xx5)/Keyword_requests_total*100))
    	        Today=conn_time.split(' ')[0]
                Insert_SQL="replace into ngx_uri(today,domain,uri,2xx,3xx,4xx,5xx,requests_total,error_rate,t0,t1,t2,t3,miss,hit,expired,ip) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" %(Today,Domain,Keyword,xx2,xx3,xx4,xx5,Keyword_requests_total,error_rate,t0,t1,t2,t3,miss,hit,expired,Ip) 
                operating_db(Insert_SQL) 

def Default_data_storage(Ip,Domain,Timespan,conn_time,start_time):
    Insert_SQL="insert into ngx_connections(ip,Timespan,active,reading,writing,waiting,total,current,conn_time,start_time) VALUES ('%s','%s','0','0','0','0','0','0','%s','%s');" %(Ip,Timespan,conn_time,start_time)
    operating_db(Insert_SQL)
    Insert_SQL="insert into ngx_flow(domain,Timespan,inbound,outbound,requests_total,ip,start_time) VALUES ('%s','%s','0','0','0','%s','%s');" %(Domain,Timespan,Ip,start_time)
    operating_db(Insert_SQL)
    Insert_SQL="insert into ngx_request_times(domain,Timespan,t0,t1,t2,t3,ip,start_time) VALUES ('%s','%s','0','0','0','0','%s','%s');" %(Domain,Timespan,Ip,start_time)
    operating_db(Insert_SQL)
    Insert_SQL="insert into ngx_status_code(domain,Timespan,2xx,3xx,4xx,5xx,ip,start_time) VALUES ('%s','%s','0','0','0','0','%s','%s');" %(Domain,Timespan,Ip,start_time)
    operating_db(Insert_SQL)

def main():
    hosts=['192.168.200.134']
    #hosts=('192.168.200.134', '192.168.200.134')
    pool = ThreadPool(processes=3)
    #pool.map(request_ngx, hosts)
    pool.map_async(request_ngx, hosts, callback=Analysis_keys)
    pool.close()
    pool.join()

if __name__ == '__main__':
    time.sleep(60 - time.localtime().tm_sec) 
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)
    # decouple from parent environment
    os.chdir("/")
    os.setsid()
    os.umask(0)
    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            print "Daemon PID %d" % pid
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)
    # start the daemon main loop
    scheduler = BlockingScheduler()
    scheduler.add_job(main,'cron',second='*/20',hour='*')
    print 'Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C')
    try:
        scheduler.start()
    except KeyboardInterrupt,SystemExit:
        scheduler.shutdown()
    #main()
