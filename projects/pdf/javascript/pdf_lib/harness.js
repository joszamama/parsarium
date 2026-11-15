const { PDFDocument } = require('pdf-lib');
async function parsePdf(data) {
  if (!data || data.length === 0 || data.length > (1 << 20)) throw new Error('input outside harness limit');
  const document = await PDFDocument.load(Buffer.from(data));
  return { pages: document.getPageCount(), title: document.getTitle() };
}
module.exports = { parsePdf };
