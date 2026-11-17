const { parseData } = require('./harness');
module.exports.fuzz = async function fuzz(data) {
  try { await parseData(data); }
  catch (error) {
    if (!['ParseRejectedError', 'InputDecodeError', 'InputLimitError'].includes(error?.name))
      throw error;
  }
};
