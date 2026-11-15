const { parseSvg } = require('./harness');

module.exports.fuzz = function fuzz(data) {
  try {
    parseSvg(data);
  } catch (error) {
    if (error instanceof TypeError || error.message === 'input outside harness limit') {
      return;
    }
    throw error;
  }
};
