#coding=utf-8
from flask import Flask, jsonify, abort, g, make_response, request , url_for
from flask.ext.restful import Api, Resource, reqparse , fields, marshal
from app import app, api,gl
from datetime import datetime
import traceback
import json
import os
from werkzeug import secure_filename

#给学生创建对应名称的仓库
@app.route('/api/exam/createRepos', methods=['POST'])
def createRepos():
    user_list = request.json.get("userList")
    project_list = request.json.get("projectList")
    if not user_list or not project_list:
        abort(400)
    failedUser = []
    for project_name in project_list:
        for gitlab_id in user_list:
            try:
                gl.user_projects.create({'name':project_name,'user_id':gitlab_id})
            except Exception,ex:
                failedUser.append(project_name + ":" + str(gitlab_id))
    return jsonify({"code":1,"failedRepo":failedUser}),200


@app.route('/api/user/createUser', methods=['POST'])
def createGitlabUser():
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        abort(400)
    try:
        glUser = gl.users.create({'email': username+"@mail.smal.nju.edu.cn",
                        'password': password,
                        'username': username,
                        'name': username})
        return jsonify({"code":1,"gitlabId":glUser.id}),200
    except Exception,ex:
        return jsonify({"code":0,"gitlabId":""}),200





#上传一个项目
@app.route('/api/exam/uploadProject', methods=['POST'])
def uploadFile():
    f = request.files['file']
    if not f:
        abort(400)
    fname = secure_filename(f.filename) #获取一个安全的文件名，且仅仅支持ascii字符；
    try:
        f.save(os.path.join("upload", fname))
    except Exception,ex:
        return jsonify({"code":0,"message":"文件保存出现问题"}),200
    return jsonify({"code":1,"gitlabUrl":""}),200

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"code":-1,"message":"缺少参数"}), 400)
