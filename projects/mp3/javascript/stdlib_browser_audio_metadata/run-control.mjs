import { writeFile } from 'node:fs/promises';
import { replay } from './replay.mjs';

const file = process.argv[2] ?? '/input/control';
const result = await replay(file);
const expected = {"duration": 1};
if (JSON.stringify(result.output) !== JSON.stringify(expected))
  throw new Error(`control mismatch: ${JSON.stringify(result.output)}`);
if (result.browser !== '153.0.8010.12')
  throw new Error(`unexpected Chromium version: ${result.browser}`);
const summary = {
  control_pass: true, output: result.output, browser: result.browser,
  adapter_js_functions_covered: result.adapterFunctionsCovered,
  adapter_coverage_scope: result.adapterCoverageScope,
  native_decoder_source_coverage: result.nativeDecoderSourceCoverage,
  parser_feedback_available: false
};
await writeFile('/coverage/observed.json', JSON.stringify(result.output, null, 2) + '\n');
await writeFile('/coverage/summary.json', JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify(summary));
