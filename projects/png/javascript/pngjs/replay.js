const fs = require('node:fs');
const { parsePng } = require('./harness');

if (process.argv.length !== 3) {
  throw new Error('expected a local control path');
}
console.log(JSON.stringify(parsePng(fs.readFileSync(process.argv[2]))));
