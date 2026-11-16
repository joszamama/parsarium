"use strict";
const { ZipBuffer, setMaxZipContentSize } = require("node:zlib");

setMaxZipContentSize(1 << 20);

async function parseData(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > (1 << 20)) return null;
  try {
    const zip = new ZipBuffer(data);
    const entries = [...zip.keys()];
    if (!entries.length) return null;
    const content = (await zip.get(entries[0]).content()).toString("utf8");
    return { entries, content };
  } catch {
    return null;
  }
}

module.exports = { parseData };
