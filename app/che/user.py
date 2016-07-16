#coding=utf-8

from flask import Flask, jsonify, abort, g, make_response, request , url_for
from flask.ext.restful import Api, Resource
from flask.ext.httpauth import HTTPBasicAuth
from sqlalchemy.orm import relationship, backref
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from app import app,db,api
import json
import workspace
from workspace import create_workspace

auth = HTTPBasicAuth()

# Model User 用户 对应表:User
# id->唯一标识
# username->用户名
# name->用户姓名
# password_hash->加密后的密码
# workspace_id->用户对应workspace_id
# user_groups->与群组的关联，即每个群组中有哪些用户，只是定义一个外键，不存在群组表中
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))
    workspace_id = db.Column(db.String(32))
    name = db.Column(db.String(32))
    user_groups = relationship("GroupRelation",backref = "User")

    def json(self):
        return {"id":self.id,"username":self.username,"workspace_id":self.workspace_id,"name":self.name}

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

# 校验密码
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

class UsersAPI(Resource):
    # 创建一个用户，创建用户的同时创建其workspace并且获取workspace_id
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        name = request.json.get('name')
        if username is None or password is None:
            abort(400)    # missing arguments
        if User.query.filter_by(username=username).first() is not None:
            abort(400)    # existing user
        # create workspace
        created_workspace = create_workspace(name)
        workspace_id = created_workspace["id"]
        user = User(username=username)
        user.hash_password(password)
        user.name = name
        user.workspace_id = workspace_id
        db.session.add(user)
        db.session.commit()
        return {'name':user.name,'username': user.username, 'workspace_id':user.workspace_id},

    # 删除用户的同时记得删除workspace
    def delete(self):
        pass

api.add_resource(UsersAPI,'/che/api/v1.0/users',endpoint = "User")


@app.route('/che/api/v1.0/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username, 'name':user.name, 'workospace_id':user.workspace_id})


@app.route('/che/api/v1.0/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(6000)
    return jsonify({'token': token.decode('ascii'), 'duration': 6000})
