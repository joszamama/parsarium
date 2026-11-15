const { parseMp4 } = require('./harness');

module.exports.fuzz = async function fuzz(data) {
  try {
    await parseMp4(data);
  } catch (error) {
    if (error.message === 'input outside harness limit' ||
        error.name === 'EndOfStreamError' ||
        error.name === 'CouldNotDetermineFileTypeError') {
      return;
    }
    throw error;
  }
};
