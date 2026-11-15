const { parseHttp } = require('./harness');
module.exports.fuzz = function fuzz(data) { parseHttp(data); };
