const { parseData } = require('./harness');
module.exports.fuzz = async function fuzz(data) {
  try { await parseData(data); }
  catch (error) {
    // Only expected parse/decode/size failures are ignored by the fuzz target.
    if (!['SyntaxError', 'InputDecodeError', 'InputLimitError'].includes(error?.name))
      throw error;
  }
};
