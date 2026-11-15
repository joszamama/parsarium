const { parsePng } = require('./harness');

const expectedError = /^(input size outside harness limit|decoded output outside harness limit|Invalid file signature|Expected IHDR|Unsupported |Crc error|Transparency chunk|More transparent colors|Expected palette not found|Unexpected end of input|unrecognised content at end of stream|Unrecognised filter type|Ran out of data|unrecognised depth|extra data found|bad png - invalid inflate data response|index \d+ not in palette)/;

module.exports.fuzz = function fuzz(data) {
  try {
    parsePng(data);
  } catch (error) {
    if (error instanceof Error && (expectedError.test(error.message) ||
        error.code === 'Z_DATA_ERROR' || error.code === 'Z_BUF_ERROR')) {
      return;
    }
    throw error;
  }
};
