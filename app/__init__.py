from flask import Flask, jsonify, abort, make_response, request , url_for
from flask.ext.restful import Api, Resource, reqparse , fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
import gitlab
import os
try:
    os.mkdir("upload")
except Exception,ex:
    print("exist")
app = Flask(__name__)
api = Api(app)
gl = gitlab.Gitlab('http://115.29.184.56:10080', 'A3BUxxUb2jNxEUxtxN3P')
from app import views
import che.exam
