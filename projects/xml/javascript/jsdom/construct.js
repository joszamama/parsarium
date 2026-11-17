const fs = require('node:fs');
const { constructData } = require('./harness');
constructData(fs.readFileSync(process.argv[2]))
  .catch(error => { console.error(error); process.exitCode = 1; });
