'use strict';

exports.examsPOST = function(args, res, next) {
  /**
   * parameters expected in the args:
  * exam (Exam)
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

