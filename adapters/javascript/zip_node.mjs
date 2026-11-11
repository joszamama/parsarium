// Node.js 26.10.0 built-in, experimental ZIP parser.
import { readFile } from 'node:fs/promises';
import { ZipBuffer } from 'node:zlib';

const path = process.argv[2];
if (!path) {
  console.error('usage: node adapters/javascript/zip_node.mjs <ZIP path>');
  process.exit(2);
}
const zip = new ZipBuffer(await readFile(path));
const entries = Array.from(zip.keys());
const content = (await zip.get(entries[0]).content()).toString('utf8');
console.log(JSON.stringify({ entries, content }));
