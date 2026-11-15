const { parsePdf } = require('./harness');
module.exports.fuzz = async function fuzz(data) {
  try { await parsePdf(data); }
  catch (error) {
    if (error.message === 'input outside harness limit' || error.name === 'MissingPDFHeaderError' ||
        error.name === 'PDFParsingError' || error.name === 'InvalidPDFError') return;
    throw error;
  }
};
