#coding:utf-8
from flask import render_template, request, current_app, redirect, url_for, flash, session
from . import main
from ..models import User, Group
#from .forms import CommentForm
from .. import db
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_login import login_required, current_user
import MySQLdb as mdb
import datetime

#class NameForm(Form):
#    name = StringField('what is your name?', validators=[Required()])
#    submit = SubmitField('Submit')


@main.route('/')
@main.route('/index')
@login_required
def index():
    User_count = User.query.count()
    Group_count = Group.query.count()
    return render_template('main/index.html', User_count=User_count, Group_count=Group_count)

@main.route('/about')
@login_required
def about():
    return render_template('main/about.html')

@main.route('/test')
def test():
    return render_template('main/test.html')





def uptime(result):
    today_now=datetime.datetime.now()
    start_time=datetime.datetime.strptime(result, '%Y-%m-%d %H:%M:%S')    
    Difference=(today_now-start_time).seconds
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

