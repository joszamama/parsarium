const { parseZip } = require('./harness');

const expectedCodes = new Set([0, 1, 2, 3, 6, 8, 13, 14]);

module.exports.fuzz = function fuzz(data) {
  try {
    parseZip(data);
  } catch (error) {
    if (error instanceof Error && (error.message === 'input size outside harness limit' ||
        expectedCodes.has(error.code))) {
      return;
    }
    throw error;
  }
};
