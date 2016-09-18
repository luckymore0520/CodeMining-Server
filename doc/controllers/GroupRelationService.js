'use strict';

exports.groupRelationGET = function(args, res, next) {
  /**
   * parameters expected in the args:
  * user_id (String)
  * group_id (String)
  **/
    var examples = {};
  examples['application/json'] = {
  "groups" : [ {
    "name" : "aeiou",
    "description" : "aeiou",
    "id" : "aeiou"
  } ],
  "users" : [ {
    "name" : "aeiou",
    "id" : "aeiou",
    "username" : "aeiou"
  } ]
};
  if(Object.keys(examples).length > 0) {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(examples[Object.keys(examples)[0]] || {}, null, 2));
  }
  else {
    res.end();
  }
  
}

exports.groupRelationPOST = function(args, res, next) {
  /**
   * parameters expected in the args:
  * json (Json_1)
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

