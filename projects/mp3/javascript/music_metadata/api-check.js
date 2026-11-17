// The documented file and stream entry points must report the same MPEG format as parseBuffer.
const fs = require('node:fs');
const { pathToFileURL } = require('node:url');

async function main() {
  const { parse, parsePath, parseReadable } = await import(pathToFileURL('/work/adapter.mjs'));
  const path = process.argv[2];
  const buffer = await parse(fs.readFileSync(path));
  const results = { parseBuffer: buffer, parseFile: await parsePath(path), parseStream: await parseReadable(path) };
  for (const [api, output] of Object.entries(results)) {
    if (JSON.stringify(output) !== JSON.stringify(buffer)) throw new Error(`${api} differs: ${JSON.stringify(output)}`);
  }
  console.log(JSON.stringify({ apis: Object.keys(results), output: buffer }));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
