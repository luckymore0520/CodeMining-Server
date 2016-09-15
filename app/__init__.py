from flask import Flask, jsonify, abort, make_response, request , url_for
from flask.ext.restful import Api, Resource, reqparse , fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy
from app import config
import gitlab

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] =  config.DB_URL
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
db = SQLAlchemy(app)
gl = gitlab.Gitlab('http://115.29.184.56:10080', 'A3BUxxUb2jNxEUxtxN3P')
from app import views
import che.user
import che.group
import che.exam
import che.project
import config
