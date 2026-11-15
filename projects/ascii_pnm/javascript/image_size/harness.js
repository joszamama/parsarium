const { imageSize } = require('image-size');

function parsePnm(data) {
  if (!data || data.length === 0 || data.length > (1 << 20)) {
    throw new Error('input outside harness limit');
  }
  const parsed = imageSize(Buffer.from(data));
  return { type: parsed.type, width: parsed.width, height: parsed.height };
}

module.exports = { parsePnm };
