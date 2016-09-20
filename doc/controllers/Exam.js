'use strict';

var url = require('url');


var Exam = require('./ExamService');


module.exports.examsExam_idDELETE = function examsExam_idDELETE (req, res, next) {
  Exam.examsExam_idDELETE(req.swagger.params, res, next);
};

module.exports.examsExam_idGET = function examsExam_idGET (req, res, next) {
  Exam.examsExam_idGET(req.swagger.params, res, next);
};

module.exports.examsGET = function examsGET (req, res, next) {
  Exam.examsGET(req.swagger.params, res, next);
};

module.exports.examsOfUserUser_idGET = function examsOfUserUser_idGET (req, res, next) {
  Exam.examsOfUserUser_idGET(req.swagger.params, res, next);
};

module.exports.examsPOST = function examsPOST (req, res, next) {
  Exam.examsPOST(req.swagger.params, res, next);
};
