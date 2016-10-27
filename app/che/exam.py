#coding=utf-8
from flask import Flask, jsonify, abort, g, make_response, request , url_for
from flask.ext.restful import Api, Resource, reqparse , fields, marshal
from app import app ,db , api,gl
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from project import Project
from group import GroupRelation,Group
from user import User
from tools import SimpleResult
from datetime import datetime
import traceback
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
    project_ids = db.Column(db.String(64))
    group_id = db.Column(db.Integer, ForeignKey('Group.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)


    def json(self):
        return {"name":self.name,"description":self.description,"project_ids":self.project_ids,"group_id":self.group_id,"id":self.id,"start_date":self.start_date.strftime('%Y-%m-%d %H:%M:%S'),"end_date":self.end_date.strftime('%Y-%m-%d %H:%M:%S')}



# TODO Gitlab 需要在用户所对应的Gitlab账户中 Fork 该项目
def configExam(exam):
    projects = exam.project_ids
    failedUser = []
    relations = GroupRelation.query.filter_by(group_id = exam.group_id).all()
    for project_id in projects:
        print(project_id)
        project = Project.query.get(project_id)
        if not project:
            return
        for relation in relations:
            user = User.query.filter_by(id = relation.user_id).first()
            try:
                gl.user_projects.create({'name':project.name,'user_id':user.gitlab_id})
            except Exception,ex:
                failedUser.append(project_id + ":" + user.username)
    return failedUser


class ExamUserAPI(Resource):
    def get(self,user_id):
        relations = GroupRelation.query.filter_by(user_id = user_id).all()
        result = []
        for relation in relations:
            exams = Exam.query.filter_by(group_id = relation.group_id)
            for exam in exams:
                result.append(exam.json())
        return result
        pass
api.add_resource(ExamUserAPI, '/che/api/v1.0/examsOfUser/<string:user_id>', endpoint = 'exams_user')

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
        project_ids = request.json.get('project_ids')
        usernames = request.json.get('usernames')
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date');
        if name is None or project_ids is None or usernames is None:
            abort(400)    # missing arguments



        group = Group()
        group.name = name
        db.session.add(group)
        db.session.commit()

        for username in usernames:
            user = User.query.filter_by(username = username).first()
            relation = GroupRelation()
            relation.group_id = group.id
            relation.user_id = user.id
            db.session.add(relation)
        db.session.commit()

        exam = Exam()
        exam.name = name
        exam.description = description
        exam.project_ids = project_ids
        exam.group_id = group.id
        exam.start_date = datetime.strptime(start_date,'%Y-%m-%d %H:%M:%S')
        exam.end_date = datetime.strptime(end_date,'%Y-%m-%d %H:%M:%S')
        exam.config = "会是一段json配置，需要显示给学生"
        failedUser = configExam(exam)
        db.session.add(exam)
        db.session.commit()
        result = exam.json()
        result["failedUser"] = failedUser
        return result

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
