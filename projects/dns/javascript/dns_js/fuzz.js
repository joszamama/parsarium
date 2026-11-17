const { parseData } = require('./harness');
module.exports.fuzz = function fuzz(data) {
  try { parseData(data); }
  catch (error) {
    // dns-js rejects malformed messages by throwing; only non-Error throws are unexpected.
    if (!(error instanceof Error)) throw error;
  }
};
