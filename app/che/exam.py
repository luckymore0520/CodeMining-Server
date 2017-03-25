#coding=utf-8
from flask import Flask, jsonify, abort, g, make_response, request , url_for
from flask.ext.restful import Api, Resource, reqparse , fields, marshal
from app import app, api,gl
from datetime import datetime
import traceback
import json
import os
import shutil
import urllib 
import urllib2 
import requests
import zipfile
import commands
from werkzeug import secure_filename

#给学生创建对应名称的仓库
@app.route('/api/exams/createRepos', methods=['POST'])
def createRepos():
    user_list = request.json.get("gitIds")
    project_list = request.json.get("projects")
    if not user_list or not project_list:
        abort(400)
    failedUser = {}
    for gitlab_id in user_list:
        for project_name in project_list:
            try:
                gl.user_projects.create({'name':project_name,'user_id':gitlab_id})
            except Exception,ex:

                if not failedUser.has_key(gitlab_id):
                    failedUser[gitlab_id] = []
                failedUser[gitlab_id].append(project_name) 
    return jsonify({"code":1,"failedRepo":failedUser}),200


@app.route('/api/users/massiveCreateWithArray', methods=['POST'])
def massiveCreateWithArray():
    users = request.json.get("users")
    for user in users:
        username = str(user)
        password = username
        try:
            glUser = gl.users.create({'email': username+"@mail.smal.nju.edu.cn",
                            'password': password,
                            'username': username,
                            'name': username})
                
        except Exception,ex:
            print("创建失败"+username)
    return jsonify({"code":1}),200

@app.route('/api/users/massiveCreate', methods=['POST'])
def massiveCreateGitlabUser():
    start = request.json.get("start")
    end = request.json.get("end")
    for i in range(int(start),int(end)):
        username = str(i)
        password = username
        try:
            glUser = gl.users.create({'email': username+"@mail.smal.nju.edu.cn",
                            'password': password,
                            'username': username,
                            'name': username})
                
        except Exception,ex:
            print("创建失败"+username)
    return jsonify({"code":1}),200

@app.route('/api/users/createUser', methods=['POST'])
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
        return jsonify({"code":1,"gitId":glUser.id}),200
    except Exception,ex:
        return jsonify({"code":0}),200


#上传一个项目
@app.route('/api/exam/uploadProject', methods=['POST'])
def uploadFile():
    project_name = request.json.get("projectName")
    url = request.json.get("fileUrl")  
    urllib.urlretrieve(url, "tmp/file.zip")
    file_zip = zipfile.ZipFile("tmp/file.zip","r")
    for file in file_zip.namelist():
        file_zip.extract(file, r'./tmp')
    file_zip.close()
    os.remove("tmp/file.zip") 
    list = os.listdir("tmp")
    dirName = list[1]
    list = os.listdir("tmp/"+dirName)
    try:
        gl.projects.create({'name': project_name})
    except Exception,ex:
        print("项目已存在")
    (status, output) = commands.getstatusoutput('cd git && git clone http://115.29.184.56:10080/root/'+project_name+".git")
    for file in list:
        shutil.move("tmp/"+dirName+"/"+file,"git/"+project_name+"/"+file) 
    shutil.copyfile("default/Login.sh","git/"+project_name+"/Login.sh")
    shutil.copyfile("default/auto-commit.sh","git/"+project_name+"/auto-commit.sh")
    (status, output) = commands.getstatusoutput('cd git/'+project_name + '&& git add * -f && git commit -m "init" && git push -u origin master')
    return jsonify({"code":1,"gitUrl":'http://115.29.184.56:10080/root/'+project_name+".git"}),200

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"code":-1,"message":"缺少参数"}), 400)
