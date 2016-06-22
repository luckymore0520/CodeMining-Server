from flask import Flask, jsonify, abort, make_response, request , url_for
from flask.ext.restful import Api, Resource, reqparse , fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy
from app import config
import config
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] =  config.DB_URL
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
db = SQLAlchemy(app)
from app import views
import che.workspace
import che.user
import che.group
import che.exam
import che.project

if __name__ == '__main__':
    #create table from up model
    print("Create All")
    db.create_all()


# @auth.get_password
# def get_password(username):
#     if username == 'miguel':
#         return 'python'
#     return None
#
# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 403)
#
#
#
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
