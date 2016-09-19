'use strict';

var url = require('url');


var Project = require('./ProjectService');


module.exports.projectIdGET = function projectIdGET (req, res, next) {
  Project.projectIdGET(req.swagger.params, res, next);
};

module.exports.projectsGET = function projectsGET (req, res, next) {
  Project.projectsGET(req.swagger.params, res, next);
};

module.exports.projectsPOST = function projectsPOST (req, res, next) {
  Project.projectsPOST(req.swagger.params, res, next);
};
