const fs = require('node:fs');
const { parseMp4 } = require('./harness');

if (process.argv.length !== 3) {
  throw new Error('expected a local control path');
}
parseMp4(fs.readFileSync(process.argv[2]))
  .then(result => console.log(JSON.stringify(result)))
  .catch(error => { console.error(error); process.exitCode = 1; });
