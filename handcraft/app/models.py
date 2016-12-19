#coding: utf-8

import hashlib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    phone = db.Column(db.String(11))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(1))
    active = db.Column(db.String(1))
    token = db.Column(db.String(128))

    @staticmethod
    def insert_admin(email, username, password, phone, role):
        user = User(email=email, username=username, phone=phone, password_hash=password, role=role, active='1')
        db.session.add(user)
        db.session.commit()

    @property
    def password(self):
        flash(u'密码不可读', 'danger')
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    comment = db.Column(db.String(64), unique=True, index=True)

class User_Group(db.Model):
    __tablename__ = 'user_group'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

# callback function for flask-login extentsion
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
