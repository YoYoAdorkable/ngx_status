# coding: utf-8
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from . import auth
from .. import db
from ..models import User, Group, User_Group
from .forms import LoginForm, RegistrationForm, EmailForm, PasswordForm, UserForm, SettingForm, GroupForm, EditorForm, AvatarForm
from .. import Config
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from ..send_mail import *
from flask_login import login_required
from sqlalchemy import desc
import math
import os, sys
import Image
import base64
reload(sys)
sys.setdefaultencoding( "utf-8" )


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            if int(user.active) == 0:
                login_user(user)
                return redirect(url_for('main.index'))
            elif int(user.active) == 1:
                flash(u'登陆失败！此用户尚未激活。', 'danger')
            else:
                flash(u'登陆失败！此用户禁止登录。', 'danger')
        else:
            flash(u'登陆失败！用户名或密码错误，请重新登陆。', 'danger')
    if form.errors:
        flash(u'登陆失败，请尝试重新登陆.', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    group_all = Group.query.all()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    phone=form.phone.data,
                    password=form.password.data,
                    role=form.role.data,
                    active=form.active.data)
        db.session.add(user)
        db.session.commit()
        userid = User.query.filter_by(username=form.username.data).first().id
        groups_post = request.values.getlist("group")
        db_add_user_group(userid,groups_post)
        flash(u'请耐心等待审批,通过后可以登录.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form, group_all = group_all)

@login_required
@auth.route('/user_add', methods=['GET', 'POST'])
def user_add():
    form = RegistrationForm()
    group_all = Group.query.all()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    phone=form.phone.data,
                    password=form.password.data,
                    role=form.role.data,
                    active=form.active.data
        )
        db.session.add(user)
        db.session.commit()
        userid = User.query.filter_by(username=form.username.data).first().id
        groups_post = request.values.getlist("group")
        db_add_user_group(userid,groups_post)
        if form.active.data == 1:
            flash(u'请耐心等待审批,通过后可以登录.', 'danger')
        return redirect(url_for('auth.user'))
    return render_template('auth/user_add.html', form=form, group_all = group_all)

def db_add_user_group(userid,groups_post):
    if groups_post:
        for group_id in groups_post:
            user_group = User_Group(user_id=userid,
                                    group_id=group_id
            )
            db.session.add(user_group)
            db.session.commit()
    
@auth.route('/reset', methods=['GET', 'POST'])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            subject = "Handcraft 密码重置"
            ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = ts.dumps(user.email, salt='recover-key')
            recover_url = url_for('auth.reset_with_token', token=token, _external=True)
            html = render_template('auth/recover.html', recover_url=recover_url, form=form)
            send_email(user.email, subject, html)
            return redirect(url_for('main.index'))
        else:
            flash(u'邮箱地址不存在。', 'danger')
    return render_template('auth/reset.html', form=form)


@auth.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = ts.loads(token, salt="recover-key", max_age=300)
    except:
        return render_template('404.html')
    form = PasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash(u'密码已经修改,请用新密码登录。', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_with_token.html', form=form, token=token)

@login_required
@auth.route('/user',methods=["GET", "POST"])
def user():
    page=int( request.args.get('page','1'))
    POSTS_PER_PAGE=10
    if page<1:
        page=1
        paginate = User.query.order_by(User.id).paginate(page, POSTS_PER_PAGE, False)
    else:
        paginate = User.query.order_by(User.id).paginate(page, POSTS_PER_PAGE, False)   
    object_list = paginate.items
    total=paginate.total
    total=total/10.0
    total=int(math.ceil(total))
    
    form = AvatarForm()
    if request.method == 'POST':
        for user_id in request.values.getlist("selected"):
            user = User.query.filter_by(id=user_id).first()
            db.session.delete(user)
            db.session.commit()
            db.session.query(User_Group).filter(User_Group.user_id==user_id).delete()
            db.session.commit()
        return redirect(url_for('auth.user'))
    
    return render_template('auth/user_list.html',pagination = paginate,object_list = object_list,POSTS_PER_PAGE=POSTS_PER_PAGE,total=total,form=form)
 
@login_required
@auth.route('/profile/<username>', methods=["GET"])
def user_profile(username):
    results = User.query.filter_by(username=username).first()
    groups = db_select_group(results)
    return render_template('auth/profile.html', results=results, groups=groups)

def db_select_group(results):
    user_group = User_Group.query.filter_by(user_id=results.id).all()
    groups = []
    for i in range(len(user_group)):
        group = Group.query.filter_by(id=user_group[i].group_id).first().name
        groups.append(group)
    return groups

@login_required
@auth.route('/setting/<username>', methods=["GET", "POST"])
def user_setting(username):
    form = SettingForm()
    group_all = Group.query.all()
    results = User.query.filter_by(username=username).first()
    groups = db_select_group(results)
    groups_post = request.values.getlist("ug")
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        user.username = form.username.data
        user.email = form.email.data
        user.phone = form.phone.data
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        db.session.query(User_Group).filter(User_Group.user_id==results.id).delete()
        db.session.commit()
        db_add_user_group(results.id,groups_post)
        return redirect(url_for('auth.user'))
    return render_template('auth/user_setting.html', results=results, form=form, group_all=group_all, groups=groups)

@login_required
@auth.route('/delete/<username>', methods=["GET", "POST"])
def delete(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    db.session.query(User_Group).filter(User_Group.user_id==user.id).delete()
    db.session.commit()
    return redirect(url_for('auth.user'))

@login_required
@auth.route('/activation/<username>', methods=["GET", "POST"])
def activation(username):
    user = User.query.filter_by(username=username).first()
    user.active = 0
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('auth.user'))

@login_required
@auth.route('/forbidden/<username>', methods=["GET", "POST"])
def forbidden(username):
    user = User.query.filter_by(username=username).first()
    user.active = 1
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('auth.user'))

@login_required
@auth.route('/group',methods=["GET"])
def group():
    results = Group.query.all()
    return render_template('auth/group_list.html', results=results)

@login_required
@auth.route('/group_add', methods=['GET', 'POST'])
def group_add():
    form = GroupForm()
    if form.validate_on_submit():
        group = Group(name=form.name.data,
                    comment=form.comment.data
        )
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('auth.group'))
    return render_template('auth/group_add.html', form=form)

@login_required
@auth.route('/editor/<name>', methods=["GET", "POST"])
def group_setting(name):
    form = EditorForm()
    results = Group.query.filter_by(name=name).first()
    if form.validate_on_submit():
        group = Group.query.filter_by(id=form.id.data).first()
        group.name = form.name.data
        group.comment = form.comment.data
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('auth.group'))
    return render_template('auth/group_setting.html', results=results, form=form)

@login_required
@auth.route('/erased/<name>', methods=["GET", "POST"])
def erased(name):
    group = Group.query.filter_by(name=name).first()
    db.session.delete(group)
    db.session.commit()
    db.session.query(User_Group).filter(User_Group.group_id==group.id).delete()
    db.session.commit()
    return redirect(url_for('auth.group'))

@login_required
@auth.route('/edit_avatar', methods=["GET", "POST"])
def avatar():
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir = os.path.join(basedir,current_app.config['UPLOAD_IMG_FOLDER'])
    username = request.values.get('username')
    form = AvatarForm()
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            size = (50, 50)
            im = Image.open(file)
            im.thumbnail(size)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                newname = username+'.jpg'
                im.save(os.path.join(file_dir, newname))
                token = base64.b64encode(newname)
                user = User.query.filter_by(username=username).first()
                user.token = token
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('main.index'))
    return render_template('auth/change_avatar.html', form=form)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@login_required
@auth.route('/logout', methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def operating_db ( sql = '' ):
    db_host = current_app.config['MYSQL_HOST']
    db_user = current_app.config['MYSQL_USER']
    db_pass = current_app.config['MYSQL_PASS']
    db_name = current_app.config['MYSQL_FLA_DB']

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
