import { readFile } from 'node:fs/promises';
import { chromium } from 'playwright';

export async function replay(file) {
  const bytes = file === '-' ? await readStdin() : await readFile(file);
  if (bytes.length === 0 || bytes.length > 1024 * 1024)
    throw new Error('input must contain 1 to 1048576 bytes');
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage();
    const cdp = await page.context().newCDPSession(page);
    await cdp.send('Profiler.enable');
    await cdp.send('Profiler.startPreciseCoverage', { callCount: true, detailed: true });
    await page.addScriptTag({ path: '/work/browser-harness.js' });
    const output = await page.evaluate(
      (input) => globalThis.parsariumParseLocal(input), Array.from(bytes));
    const coverage = await cdp.send('Profiler.takePreciseCoverage');
    const scripts = coverage.result.filter((script) =>
      script.url.endsWith('/work/browser-harness.js'));
    const adapterFunctionsCovered = scripts.reduce((sum, script) =>
      sum + script.functions.filter((fn) => fn.ranges.some((r) => r.count > 0)).length, 0);
    if (adapterFunctionsCovered === 0)
      throw new Error('V8 did not record executed browser harness functions');
    return {
      output,
      browser: browser.version(),
      adapterFunctionsCovered,
      adapterCoverageScope: 'browser-harness.js only',
      nativeDecoderSourceCoverage: 'unavailable'
    };
  } finally {
    await browser.close();
  }
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks);
}

if (process.argv[1] === '/work/replay.mjs') {
  const file = process.argv[2];
  if (!file) throw new Error('usage: node /work/replay.mjs FILE|-');
  const result = await replay(file);
  console.log(JSON.stringify(result.output));
}
