const { parseData } = require('./harness');
module.exports.fuzz = async function fuzz(data) {
  try { await parseData(data); }
  catch (error) { if (!(error instanceof Error)) throw error; }
};
