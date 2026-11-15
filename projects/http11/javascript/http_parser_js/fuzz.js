const { parseHttp } = require('./harness');
module.exports.fuzz = function fuzz(data) {
  if (!data || data.length === 0 || data.length > (1 << 20)) return;
  parseHttp(data);
};
