const { parseData } = require('./harness');
module.exports.fuzz = function fuzz(data) {
  try { parseData(data); }
  catch (error) {
    // native-dns-packet rejects malformed messages by throwing; only non-Error throws are unexpected.
    if (!(error instanceof Error)) throw error;
  }
};
