const fs = require('node:fs');
const { parsePly } = require('./harness');
if (process.argv.length !== 3) throw new Error('expected control path');
parsePly(fs.readFileSync(process.argv[2]))
  .then(result => console.log(JSON.stringify(result)))
  .catch(error => { console.error(error); process.exitCode = 1; });
