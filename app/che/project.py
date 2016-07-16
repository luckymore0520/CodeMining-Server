from flask import Flask, jsonify, abort, g, make_response, request , url_for
from flask.ext.restful import Api, Resource, reqparse , fields, marshal
from app import app ,db , api
import json
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref



class Project(db.Model):
    __tablename__ = 'Project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.Text)
    url = db.Column(db.String(128))

    def json(self):
        return jsonify({"name":self.name,"description":self.description,"url":self.url,"id":self.id})

class ProjectAPI(Resource):
    def get(self,project_id):
        project = Project.query.get(project_id)
        if not project:
            abort(400)
        else:
            return project.json()
api.add_resource(ProjectAPI, '/che/api/v1.0/project/<string:project_id>', endpoint = 'Project')

class ProjectsAPI(Resource):
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
