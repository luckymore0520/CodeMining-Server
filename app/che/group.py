#coding=utf-8
from flask import Flask, jsonify, abort, g, make_response, request , url_for
from flask.ext.restful import Api, Resource
from app import app ,db , api
from user import User
import json
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

# Model Group 群组 对应表:Group
# id->唯一标识
# name->群组名称
# description->群组描述
# group_users->与用户的关联，即每个群组中有哪些用户，只是定义一个外键，不存在群组表中
class Group(db.Model):
    __tablename__ = 'Group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.Text)
    group_users = relationship("GroupRelation", backref = "Group")

    def json(self):
        return {"name":self.name,"description":self.description,"id":self.id}

# Model GroupRelation 群组关系 对应表：GroupRelation
# id->唯一标识
# group_id->群组id 对应Group表主键
# user_id->用户id 对应User表主键
class GroupRelation(db.Model):
    __tablename__ = 'GroupRelation'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, ForeignKey('Group.id'))
    user_id = db.Column(db.Integer, ForeignKey('User.id'))


# 群组相关API
class GroupAPI(Resource):
    # 获取群组
    def get(self):
        result = db.session.query(Group).all()
        tmp = []
        for group in result:
            tmp.append(group.json())
        return tmp
        pass
    # 创建群组
    def post(self):
        if not request.json or not 'name' in request.json:
            abort(400) #参数缺少
        name = request.json['name']
        if Group.query.filter_by(name=name).first() is not None:
            abort(409) #已有群组
        description = request.json['description']
        group = Group()
        group.name = name
        group.description = description
        db.session.add(group)
        db.session.commit()
        return group.json()
        pass

    # # 修改群组
    # def put(self):
    #     pass
    # # 删除群组
    # def delete(self):
    #     pass
api.add_resource(GroupAPI, '/che/api/v1.0/groups', endpoint = 'groups')


# 群组成员相关API
class GroupRelationAPI(Resource):
    # 获取用户所在群组列表或者群组中用户列表
    # 根据get参数确定，若传user_id 则返回群组列表， 若传group_id 则返回用户列表
    def get(self):
        user_id = request.args.get('user_id',0)
        group_id = request.args.get('group_id',0)
        
        if user_id != 0:
            relations = GroupRelation.query.filter_by(user_id=user_id)
            groups = []
            for relation in relations:
                group = Group.query.get(relation.group_id)
                if group:
                    groups.append(group.json())
            return {"groups":groups}
        if group_id != 0:
            relations = GroupRelation.query.filter_by(group_id=group_id)
            users = []
            for relation in relations:
                user = User.query.get(relation.user_id)
                if user:
                    users.append(user.json())
            return {"users":users}
        abort(400)
        pass

    # 向群组中添加群成员
    def post(self):
        if not request.json or not 'user_id' in request.json or not 'group_id' in request.json:
            abort(400)
        user_id = request.json['user_id']
        group_id = request.json['group_id']
        group_relation = GroupRelation()
        group_relation.group_id = group_id
        group_relation.user_id = user_id
        db.session.add(group_relation)
        result = db.session.commit()
        return {"result":1, "message":"success！"}
        pass

    def delete(self):
        pass

api.add_resource(GroupRelationAPI, '/che/api/v1.0/groupRelation',endpoint = 'groupRelation')

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': '缺少参数'}), 400)

@app.errorhandler(409)
def duplicate_group(error):
    return make_response(jsonify({'error': '群组名重复'}), 409)
