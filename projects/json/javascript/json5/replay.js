// `replay.js FILE` prints the summary; `replay.js --tree FILE` also prints the
// type-tagged tree of the value JSON5.parse returned.
const fs = require('node:fs');
const { pathToFileURL } = require('node:url');
const withTree = process.argv[2] === '--tree';
const input = fs.readFileSync(process.argv[withTree ? 3 : 2]);
import(pathToFileURL('/work/adapter.mjs'))
  .then(({ parse, decode }) => console.log(JSON.stringify(withTree ? decode(input) : parse(input))))
  .catch(error => { console.error(error); process.exitCode = 1; });
