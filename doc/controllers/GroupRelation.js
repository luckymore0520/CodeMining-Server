'use strict';

var url = require('url');


var GroupRelation = require('./GroupRelationService');


module.exports.groupRelationGET = function groupRelationGET (req, res, next) {
  GroupRelation.groupRelationGET(req.swagger.params, res, next);
};

module.exports.groupRelationPOST = function groupRelationPOST (req, res, next) {
  GroupRelation.groupRelationPOST(req.swagger.params, res, next);
};
