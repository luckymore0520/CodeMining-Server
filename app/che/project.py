#coding=utf-8

from flask import Flask, jsonify, abort, g, make_response, request , url_for
from flask.ext.restful import Api, Resource, reqparse , fields, marshal
from app import app ,db , api
import json
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


# Model Project 群组 对应表:Project
# id->唯一标识
# name->项目名称
# description->项目描述
# url->项目的url
class Project(db.Model):
    __tablename__ = 'Project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.Text)
    url = db.Column(db.String(128))

    def json(self):
        return jsonify({"name":self.name,"description":self.description,"url":self.url,"id":self.id})

class ProjectAPI(Resource):
    # 根据项目id获取项目详情
    def get(self, project_id):
        project = Project.query.get(project_id)
        if not project:
            abort(400)
        else:
            return project.json()

    # 根据项目id删除项目
    # def delete(self,project_id):
    #     pass

    # 根据项目id更新项目
    # def put(self,project_id):
    #     pass
api.add_resource(ProjectAPI, '/che/api/v1.0/project/<string:project_id>', endpoint = 'Project')


class ProjectsAPI(Resource):
    #添加项目
    def post(self):
        name = request.json.get('name')
        description = request.json.get('description')
        url = request.json.get('url')
        if name is None or url is None:
            abort(400)    # missing arguments
        if Project.query.filter_by(name=name).first() is not None:
            abort(400)
        project = Project()
        project.name = name
        project.description = description
        project.url = url
        db.session.add(project)
        db.session.commit()
        return project.json()
api.add_resource(ProjectsAPI, '/che/api/v1.0/projects', endpoint = 'Projects')

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': '缺少参数'}), 400)
