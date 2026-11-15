const fs = require('node:fs');
const { parseHttp } = require('./harness');
if (process.argv.length !== 3) throw new Error('expected control path');
const observed = parseHttp(fs.readFileSync(process.argv[2]));
if (!observed) throw new Error('HTTP parser rejected valid control');
console.log(JSON.stringify(observed));
