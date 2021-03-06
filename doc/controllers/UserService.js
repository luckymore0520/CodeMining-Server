'use strict';

exports.usersGET = function(args, res, next) {
  /**
   * parameters expected in the args:
  * page (Integer)
  * limit (Integer)
  **/
    var examples = {};
  examples['application/json'] = [ {
  "name" : "aeiou",
  "id" : "aeiou",
  "username" : "aeiou"
} ];
  if(Object.keys(examples).length > 0) {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(examples[Object.keys(examples)[0]] || {}, null, 2));
  }
  else {
    res.end();
  }
  
}

exports.usersIdGET = function(args, res, next) {
  /**
   * parameters expected in the args:
  **/
    var examples = {};
  examples['application/json'] = {
  "name" : "aeiou",
  "id" : "aeiou",
  "username" : "aeiou"
};
  if(Object.keys(examples).length > 0) {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(examples[Object.keys(examples)[0]] || {}, null, 2));
  }
  else {
    res.end();
  }
  
}

exports.usersPOST = function(args, res, next) {
  /**
   * parameters expected in the args:
  * json (Json_4)
  **/
    var examples = {};
  examples['application/json'] = {
  "name" : "aeiou",
  "id" : "aeiou",
  "username" : "aeiou"
};
  if(Object.keys(examples).length > 0) {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(examples[Object.keys(examples)[0]] || {}, null, 2));
  }
  else {
    res.end();
  }
  
}

