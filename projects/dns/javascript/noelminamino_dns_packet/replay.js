const fs = require('node:fs');
const { parseData } = require('./harness');
try {
  console.log(JSON.stringify(parseData(fs.readFileSync(process.argv[2]))));
} catch (error) {
  console.error(error);
  process.exitCode = 1;
}
