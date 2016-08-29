#coding=utf-8
from flask import Flask, jsonify, abort, g, make_response, request , url_for
from flask.ext.restful import Api, Resource, reqparse , fields, marshal
from app import app ,db , api
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from project import Project
from group import GroupRelation
from user import User
from workspace import change_workspace_state
from workspace import create_project_in_workspace
import json

# Model Exam 群组 对应表:Exam
# id->唯一标识
# name->考试名称
# description->考试描述
# project_id->与项目的关联，即考试所使用到的项目
# group_id-> 与群组的关键，考试所进行的群组
class Exam(db.Model):
    __tablename__ = 'Exam'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.Text)
    project_id = db.Column(db.Integer, ForeignKey('Project.id'))
    group_id = db.Column(db.Integer, ForeignKey('Group.id'))

    def json(self):
        return jsonify({"name":self.name,"description":self.description,"project_id":self.project_id,"group_id":self.group_id,"id":self.id})



# 这里配置考试包括获取群组中的每个成员，在成员所在的workspace中创建项目
# TODO Gitlab 需要在用户所对应的Gitlab账户中 Fork 该项目
def configExam(exam):
    project = Project.query.get(exam.project_id)
    if not project:
        return
    relations = GroupRelation.query.filter_by(group_id = exam.group_id).all()
    for relation in relations:
        user = User.query.filter_by(id = relation.user_id).first()
        if user:
            create_project_in_workspace(user.workspace_id, project.url, project.name,0)


class ExamsAPI(Resource):
    def post(self):
        name = request.json.get('name')
        description = request.json.get('description')
        project_id = request.json.get('project_id')
        group_id = request.json.get('group_id')
        if name is None or project_id is None or group_id is None:
            abort(400)    # missing arguments
        if Exam.query.filter_by(name=name).first() is not None:
            abort(400)
        exam = Exam()
        exam.name = name
        exam.description = description
        exam.project_id = project_id
        exam.group_id = group_id
        db.session.add(exam)
        db.session.commit()
        configExam(exam)
        return exam.json()
api.add_resource(ExamsAPI, '/che/api/v1.0/exams', endpoint = 'Exams')
