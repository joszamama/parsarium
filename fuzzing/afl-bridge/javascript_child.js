const fs = require('node:fs');

async function main() {
  const data = fs.readFileSync(process.argv[2]);
  await require('/work/fuzz.js').fuzz(data);
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
