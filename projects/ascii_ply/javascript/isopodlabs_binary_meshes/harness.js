// Byte input reaches the documented @isopodlabs/binary_meshes adapter branch.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

async function parseData(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > (1 << 20))
    throw new Error('input outside harness limit');
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'parsarium-'));
  const source = path.join(directory, 'input.ply');
  try {
    fs.writeFileSync(source, data);
    const { parse } = await import(pathToFileURL('/work/adapter.mjs'));
    return await parse("@isopodlabs/binary_meshes", source);
  } finally { fs.rmSync(directory, { recursive: true, force: true }); }
}
module.exports = { parseData };
