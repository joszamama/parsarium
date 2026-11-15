const fs = require('node:fs');
const { parsePnm } = require('./harness');

if (process.argv.length !== 3) {
  throw new Error('expected a local control path');
}
console.log(JSON.stringify(parsePnm(fs.readFileSync(process.argv[2]))));
