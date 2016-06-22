#coding=utf-8
from flask import Flask, jsonify, abort, make_response, request , url_for
from flask.ext.restful import Api, Resource, reqparse , fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from app import app, api
from app import config
import json
import requests
import os

def post(url,data):
    command = 'curl -X POST --header \'Content-Type: application/json\' --header \'Accept: application/json\' -d \'%s\' %s'%(json.dumps(data),url)
    print(command)
    result = os.popen(command).readlines()[0]
    print(result)
    return json.loads(result)

def get_workspace_list(skipCount,maxItems):
    response = requests.get('http://localhost:8080/api/workspace', params = {'skipCount':skipCount, 'maxItems':maxItems})
    return response.json()

def create_workspace(name):
    recipeData = {"type":"docker","name":"generated-Java","permissions":{"groups":[{"name":"public","acl":["read"]}],"users":{}},"script":"FROM codenvy/ubuntu_jdk8"}
    recipeUrl = "http://localhost:8080/api/recipe"
    result = post(recipeUrl,recipeData)
    scriptUrl = result["links"][0]["href"]
    workspace = {"environments":[{"name":name,"machineConfigs":[{"name":"ws-machine","limits":{"ram":1000},"type":"docker","source":{"location":scriptUrl,"type":"dockerfile"},"dev":True}]}],"name":name,"defaultEnv":name}
    workspaceUrl = 'http://localhost:8080/api/workspace?account=&attribute=stackId:java-default'
    return post(workspaceUrl,workspace)


def create_project_in_workspace(workspace_id, project_url, project_name):
    print("lalalalalalal")
    workspace_list =  get_workspace_list(0,1000)
    print(workspace_list)
    workspace = list(filter(lambda workspace: workspace["id"] == workspace_id,workspace_list))
    if len(workspace) > 0:
        url = workspace[0]["runtime"]["devMachine"]["runtime"]["servers"]["4401/tcp"]["url"]
        post('%s/project/%s/import/%s'%(url,workspace_id,project_name),{"location":project_url,"parameters":{},"type":"git"})


def change_workspace_state(workspace_id, workspace_name, command):
    if command == 1:
        response = post('%sworkspace/%s/runtime?environment=%s'%(config.cheHost,workspace_id,workspace_name), {})
        print(response)
        return response
    else:
        response = requests.delete('%sworkspace/%s/runtime'%(config.cheHost,workspace_id))
        if r.status_code == 204:
            return {"result":"success"},200
        else:
            return {"result":"failed"},200




class WorkspaceStateAPI(Resource):
    def get(self, workspace_id, workspace_name, command):
        return change_workspace_state(workspace_id,workspace_name,command)
api.add_resource(WorkspaceStateAPI, '/che/api/v1.0/workspaces/<string:workspace_name>/<string:workspace_id>/<int:command>', endpoint = 'workspaceState')


class WorkspaceAPI(Resource):
    def delete(self, workspace_id):
        response = requests.delete('http://localhost:8080/api/workspace/%s'%(workspaceId))
        return response.json()
        pass
api.add_resource(WorkspaceAPI, '/che/api/v1.0/workspaces/<string:workspace_id>', endpoint = 'workspace')



class WorkspaceListAPI(Resource):
    def get(self):
        skipCount = request.args.get('skipCount','0')
        maxItems = request.args.get('maxItems','30')
        return get_workspace_list(skipCount,maxItems)
        pass

    def post(self):
        if not request.json or not 'name' in request.json:
            abort(400)
        name = request.json['name']
        return create_workspace(name)
        pass
api.add_resource(WorkspaceListAPI, '/che/api/v1.0/workspaces/', endpoint = 'workspaces')
