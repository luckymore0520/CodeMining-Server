#coding=utf-8
from flask import Flask, jsonify, abort, g, make_response, request , url_for
from flask.ext.restful import Api, Resource, reqparse , fields, marshal
from app import app ,db , api
import json
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

class Group(db.Model):
    __tablename__ = 'Group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.Text)
    group_users = relationship("GroupRelation", backref = "Group")

    def json(self):
        return jsonify({"name":self.name,"description":self.description,"id":self.id})

class GroupRelation(db.Model):
    __tablename__ = 'GroupRelation'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, ForeignKey('Group.id'))
    user_id = db.Column(db.Integer, ForeignKey('User.id'))


@app.route('/che/api/v1.0/groups', methods=['POST'])
def create_group():
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

@app.route('/che/api/v1.0/groups/addUser', methods=['POST'])
def add_user():
    if not request.json or not 'user_id' in request.json or not 'group_id' in request.json:
        abort(400)
    user_id = request.json['user_id']
    group_id = request.json['group_id']
    group_relation = GroupRelation()
    group_relation.group_id = group_id
    group_relation.user_id = user_id
    db.session.add(group_relation)
    result = db.session.commit()
    print(result)
    return jsonify({"result":"success"}),200

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': '缺少参数'}), 400)

@app.errorhandler(409)
def duplicate_group(error):
    return make_response(jsonify({'error': '群组名重复'}), 409)
