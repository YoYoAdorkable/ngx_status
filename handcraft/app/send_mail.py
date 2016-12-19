# coding: utf-8

from flask import current_app, flash
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(mailto, subject, content):
    mail_host = current_app.config['MAIL_SERVER']
    mail_user = current_app.config['MAIL_USERNAME']
    mail_pass = current_app.config['MAIL_PASSWORD']
    mail_postfix = current_app.config['MAIL_POSTFIX']
    
    '''
    mailto_list:发给谁
    sub:主题
    content:内容
    send_mail("1221@163.com","sub","content")
    '''
    #me=mail_user
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = Header(me, 'utf-8')
    msg['To'] = Header(mailto, 'utf-8')
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, mailto, msg.as_string())
        s.close()
        message=u'邮件已经发送至:'+mailto
        flash(message, 'danger')
        return True
    except Exception, e:
        print str(e)
        return False
