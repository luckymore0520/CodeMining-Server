#coding=utf-8
from flask import Flask, jsonify, abort, g, make_response, request , url_for
from flask.ext.restful import Api, Resource, reqparse , fields, marshal
from app import app ,db , api,gl
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from project import Project
from group import GroupRelation
from user import User
from tools import SimpleResult
from datetime import datetime
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
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    config = db.Column(db.Text)


    def json(self):
        return {"name":self.name,"description":self.description,"project_id":self.project_id,"group_id":self.group_id,"id":self.id,"start_date":self.start_date.strftime('%Y-%m-%d %H:%M:%S'),"end_date":self.end_date.strftime('%Y-%m-%d %H:%M:%S'), "config":self.config}



# TODO Gitlab 需要在用户所对应的Gitlab账户中 Fork 该项目
def configExam(exam):
    project = Project.query.get(exam.project_id)
    if not project:
        return
    relations = GroupRelation.query.filter_by(group_id = exam.group_id).all()
    for relation in relations:
        user = User.query.filter_by(id = relation.user_id).first()
        gl.user_projects.create({'name':project.name,'user_id':user.gitlab_id})


class ExamAPI(Resource):
    def get(self,exam_id):
        exam = Exam.query.get(exam_id)
        if not exam:
            return {}
        else:
            return exam.json()
        pass

    def delete(self, exam_id):
        exam = Exam.query.get(exam_id)
        db.session.delete(exam)
        db.session.commit()
        return SimpleResult().json()

api.add_resource(ExamAPI, '/che/api/v1.0/exams/<string:exam_id>', endpoint = 'exams')

class ExamsAPI(Resource):
    #新建一场考试
    def post(self):
        name = request.json.get('name')
        description = request.json.get('description')
        project_id = request.json.get('project_id')
        group_id = request.json.get('group_id')
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date');

        if name is None or project_id is None or group_id is None:
            abort(400)    # missing arguments
        if Exam.query.filter_by(name=name).first() is not None:
            abort(400)
        exam = Exam()
        exam.name = name
        exam.description = description
        exam.project_id = project_id
        exam.group_id = group_id
        exam.start_date = datetime.strptime(start_date,'%Y-%m-%d %H:%M:%S')
        exam.end_date = datetime.strptime(end_date,'%Y-%m-%d %H:%M:%S')
        exam.config = "会是一段json配置，需要显示给学生"
        db.session.add(exam)
        db.session.commit()
        configExam(exam)
        return exam.json()

    #获取考试，若有参数group_id，则或许特定群组的考试，否则获取全部
    def get(self):
        group_id = request.args.get('group_id',0)
        result = []
        if group_id == 0:
            result = db.session.query(Exam).all()
        else:
            result = Exam.query.filter_by(group_id = group_id)
        tmp = []
        print(result)
        for exam in result:
            tmp.append(exam.json())
        return tmp


api.add_resource(ExamsAPI, '/che/api/v1.0/exams', endpoint = 'Exams')
