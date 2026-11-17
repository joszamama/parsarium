// `replay.js FILE` prints the typed tree (sorted keys) built from the values j-toml returned.
const fs = require('node:fs');
const { pathToFileURL } = require('node:url');
const input = fs.readFileSync(process.argv[2]);
import(pathToFileURL('/work/adapter.mjs'))
  .then(({ decode, canonical }) => console.log(canonical(decode(input))))
  .catch(error => { console.error(error); process.exitCode = 1; });
