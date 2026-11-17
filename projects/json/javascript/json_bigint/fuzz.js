const { parseData } = require('./harness');
module.exports.fuzz = async function fuzz(data) {
  try { await parseData(data); }
  catch (error) {
    // json-bigint throws a plain SyntaxError-shaped object on parse failures.
    if (!['SyntaxError', 'InputDecodeError', 'InputLimitError'].includes(error?.name))
      throw error;
  }
};
