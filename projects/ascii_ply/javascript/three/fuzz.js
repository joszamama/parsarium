const { parsePly } = require('./harness');
module.exports.fuzz = async function fuzz(data) { await parsePly(data); };
