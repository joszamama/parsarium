const fs = require('node:fs');
const { parseData } = require('./harness');
parseData(fs.readFileSync(process.argv[2])).then(value => console.log(JSON.stringify(value)))
  .catch(error => { console.error(error); process.exitCode = 1; });
