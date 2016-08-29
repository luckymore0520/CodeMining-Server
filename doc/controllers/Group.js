'use strict';

var url = require('url');


var Group = require('./GroupService');


module.exports.groupsGET = function groupsGET (req, res, next) {
  Group.groupsGET(req.swagger.params, res, next);
};

module.exports.groupsPOST = function groupsPOST (req, res, next) {
  Group.groupsPOST(req.swagger.params, res, next);
};
