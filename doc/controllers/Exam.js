'use strict';

var url = require('url');


var Exam = require('./ExamService');


module.exports.examsPOST = function examsPOST (req, res, next) {
  Exam.examsPOST(req.swagger.params, res, next);
};
