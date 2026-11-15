const { parseWav } = require('./harness');

module.exports.fuzz = async function fuzz(data) {
  try {
    await parseWav(data);
  } catch (error) {
    if (error.message === 'input outside harness limit' ||
        error.name === 'EndOfStreamError' ||
        error.name === 'CouldNotDetermineFileTypeError') {
      return;
    }
    throw error;
  }
};
