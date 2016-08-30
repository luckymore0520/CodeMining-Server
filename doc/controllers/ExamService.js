'use strict';

exports.examsExam_idDELETE = function(args, res, next) {
  /**
   * parameters expected in the args:
  **/
    var examples = {};
  examples['application/json'] = {
  "result" : 123,
  "message" : "aeiou"
};
  if(Object.keys(examples).length > 0) {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(examples[Object.keys(examples)[0]] || {}, null, 2));
  }
  else {
    res.end();
  }
  
}

exports.examsExam_idGET = function(args, res, next) {
  /**
   * parameters expected in the args:
  **/
    var examples = {};
  examples['application/json'] = {
  "group_id" : "aeiou",
  "project_id" : "aeiou",
  "name" : "aeiou",
  "description" : "aeiou",
  "id" : "aeiou"
};
  if(Object.keys(examples).length > 0) {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(examples[Object.keys(examples)[0]] || {}, null, 2));
  }
  else {
    res.end();
  }
  
}

exports.examsGET = function(args, res, next) {
  /**
   * parameters expected in the args:
  * group_id (String)
  **/
    var examples = {};
  examples['application/json'] = [ {
  "group_id" : "aeiou",
  "project_id" : "aeiou",
  "name" : "aeiou",
  "description" : "aeiou",
  "id" : "aeiou"
} ];
  if(Object.keys(examples).length > 0) {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(examples[Object.keys(examples)[0]] || {}, null, 2));
  }
  else {
    res.end();
  }
  
}

exports.examsPOST = function(args, res, next) {
  /**
   * parameters expected in the args:
  * name (Name)
  **/
    var examples = {};
  examples['application/json'] = {
  "group_id" : "aeiou",
  "project_id" : "aeiou",
  "name" : "aeiou",
  "description" : "aeiou",
  "id" : "aeiou"
};
  if(Object.keys(examples).length > 0) {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(examples[Object.keys(examples)[0]] || {}, null, 2));
  }
  else {
    res.end();
  }
  
}

