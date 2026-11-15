const { PNG } = require('pngjs');

function parsePng(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > (1 << 20)) {
    throw new Error('input size outside harness limit');
  }
  const image = PNG.sync.read(data, { checkCRC: true });
  if (image.width <= 0 || image.height <= 0 || image.width * image.height > (1 << 22)) {
    throw new Error('decoded output outside harness limit');
  }
  return {
    width: image.width,
    height: image.height,
    rgba: Array.from(image.data.subarray(0, 8)),
  };
}

module.exports = { parsePng };
