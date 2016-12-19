# coding: utf-8 
import os,sys 
import MySQLdb as mdb 
def operating_db ( sql = '' ): 
    db_host = '192.168.200.125' 
    db_user = 'root' 
    db_pass = '1qaz2wsx' 
    db_name = 'ngx_status'

    con = mdb.connect(db_host, db_user, db_pass, db_name , charset="utf8")

    try: 
        with con:
            cur = con.cursor()
            #cur = con.cursor(mdb.cursors.DictCursor)
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
    
#SELECT_SQL="SELECT right(Timespan,8),inbound,outbound FROM ngx_flow where ip = '192.168.200.134' and domain = 'www.yoyohandcraft.cn' ORDER BY Timespan DESC LIMIT 30"
SELECT_SQL="SELECT right(Timespan,8),2xx,3xx,4xx,5xx FROM ngx_status_code where ip = '192.168.200.134' and domain = 'www.yoyohandcraft.cn' ORDER BY Timespan DESC LIMIT 9"
Result = operating_db(SELECT_SQL)
print Result
#Times = []
#Inbounds = []
#Outbounds = []
#for i in Result:
#    Times.append(list(i)[0])
#    Inbounds.append(list(i)[1])
#    Outbounds.append(list(i)[2])
#
#Timespan = list(reversed(Times)) 
#Inbound = list(reversed(Inbounds)) 
#Outbound = list(reversed(Outbounds))
#
#r_dict= {}
#keys=[Timespan,Inbound,Outbound]
#key=['Timespan','Inbound','Outbound']
#for k in key:
#    r_dict[k]= keys[key.index(k)]
#print r_dict
