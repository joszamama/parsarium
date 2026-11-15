const fs = require('node:fs');
const { parseMp3 } = require('./harness');

if (process.argv.length !== 3) {
  throw new Error('expected a local control path');
}
parseMp3(fs.readFileSync(process.argv[2]))
  .then(result => console.log(JSON.stringify(result)))
  .catch(error => { console.error(error); process.exitCode = 1; });
