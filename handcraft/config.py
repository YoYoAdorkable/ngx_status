import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    # DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = 'mysql://handcraft:2yV96k5475@192.168.200.123/handcraft'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('mysql://root:@127.0.0.1/handcraft')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    ARTICLES_PER_PAGE = 10
    COMMENTS_PER_PAGE = 6
    SECRET_KEY = 'secret key to protect from csrf'
    WTF_CSRF_SECRET_KEY = 'random key for form' 
    # for csrf protection
    # Take good care of 'SECRET_KEY' and 'WTF_CSRF_SECRET_KEY', if you use the
    # bootstrap extension to create a form, it is Ok to use 'SECRET_KEY',
    # but when you use tha style like '{{ form.name.labey }}:{{ form.name() }}',
    # you must do this for yourself to use the wtf, more about this, you can
    # take a reference to the book <<Flask Framework Cookbook>>.
    # But the book only have the version of English.

    MAIL_SERVER = 'smtp.exmail.kuyun.com'
    MAIL_PORT = '25'
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'handcraft'
    MAIL_PASSWORD = '2yV96k5475'
    MAIL_POSTFIX = "exmail.kuyun.com"



    #MAIL_SERVER = 'smtp.qq.com'
    #MAIL_PORT = '25'
    #MAIL_USE_TLS = True
    #MAIL_USERNAME = 'yu.hailong@kuyun.com'
    #MAIL_PASSWORD = 'tenfen1234'
    #MAIL_POSTFIX = "kuyun.com"


    # nginx lua mysql
    MYSQL_HOST = '192.168.200.123'
    MYSQL_USER = 'handcraft'
    MYSQL_PASS = '2yV96k5475'
    MYSQL_PORT = '3306'
    MYSQL_NGX_DB = 'ngx_status'
    MYSQL_FLA_DB = 'handcraft'

    
    # Upload IMG
    UPLOAD_IMG_FOLDER = '/Users/yuhl/Documents/Develop/flask/handcraft/app/static/img/avatars' 
    ALLOWED_EXTENSIONS = ['txt','png','jpg','xls','JPG','PNG','xlsx','gif','GIF']






    @staticmethod
    def init_app(app):
        pass
