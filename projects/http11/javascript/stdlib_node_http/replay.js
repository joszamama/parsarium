"use strict";
const fs = require("node:fs");
const { parseData } = require("./harness");
parseData(fs.readFileSync(process.argv[2])).then(result => {
  process.stdout.write(JSON.stringify(result) + "\n");
}).catch(error => { console.error(error); process.exitCode = 1; });
