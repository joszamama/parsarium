const { parsePly } = require('./harness');
module.exports.fuzz = async function fuzz(data) {
  if (!data || data.length === 0 || data.length > (1 << 20)) return;
  await parsePly(data);
};
