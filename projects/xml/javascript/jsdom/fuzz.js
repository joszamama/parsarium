const { constructData } = require('./harness');
module.exports.fuzz = async function fuzz(data) {
  try { await constructData(data); }
  catch (error) { if (!(error instanceof Error)) throw error; }
};
