import { readFile } from 'node:fs/promises';

const [name, control] = process.argv.slice(2);
if (!name || !control) throw new Error('usage: node adapters/javascript/http11.mjs PACKAGE CONTROL_PATH');
const bytes = await readFile(control);
const string = bytes.toString('utf8');
const request = (method, target) => ({ method, target });
const response = (status, body) => ({ status, body });
let output;

if (['http-parser-js', '@achingbrain/http-parser-js', '@frida/http-parser-js', '@browsery/http-parser', '@kylecarbs/http-parser-js'].includes(name)) {
  const { HTTPParser } = await import(name);
  const parser = new HTTPParser(HTTPParser.REQUEST);
  let info;
  parser[HTTPParser.kOnHeadersComplete] = (value) => { info = value; };
  const used = parser.execute(bytes);
  if (used !== bytes.length || !info) throw new Error(`${name} did not parse the complete request`);
  output = request(HTTPParser.methods[info.method], info.url);
} else if (name === 'http-parser-ts') {
  const { HTTPParser } = await import(name);
  const parser = new HTTPParser();
  parser.initialize(HTTPParser.REQUEST);
  let info;
  parser[HTTPParser.kOnHeaders] = () => {};
  parser[HTTPParser.kOnHeadersComplete] = (...args) => { info = args; };
  parser[HTTPParser.kOnBody] = () => {};
  parser[HTTPParser.kOnMessageComplete] = () => {};
  const used = parser.execute(bytes);
  if (used !== bytes.length || !info) throw new Error('http-parser-ts did not parse the complete request');
  output = request(HTTPParser.methods[info[3]], info[4]);
} else if (name === 'http-z') {
  const { parse } = await import(name);
  const result = parse(string);
  output = request(result.method, result.target);
} else if (name === 'http-string-parser') {
  const { parseRequest } = await import(name);
  const result = parseRequest(string);
  output = request(result.method, result.uri);
} else if (['http-message-parser', '@ibiwan/http-message-parser'].includes(name)) {
  const { default: parse } = await import(name);
  const result = parse(bytes);
  output = request(result.method, result.url);
} else if (name === 'http-headers') {
  const { default: parse } = await import(name);
  const result = parse(bytes);
  output = request(result.method, result.url);
} else if (name === 'raw-http-parser') {
  const { HTTPRequest } = await import(name);
  const result = new HTTPRequest(bytes);
  output = request(result.method, result.path);
} else if (name === 'raw-request-parser') {
  const { RawRequestParser } = await import(name);
  const result = RawRequestParser.fromString(string);
  if (!result) throw new Error('raw-request-parser returned no request');
  const url = new URL(result.url);
  output = request(result.method, url.pathname + url.search);
} else if (name === 'parse-raw-http') {
  const { parseResponse } = await import(name);
  const result = parseResponse.parseResponse(bytes, { decodeContentEncoding: true });
  output = response(result.statusCode, result.bodyData.toString('utf8'));
} else if (name === '@browsercore/http1') {
  const { parseResponse } = await import(name);
  const result = parseResponse(bytes);
  if (result.bytesConsumed !== bytes.length) throw new Error('browsercore did not consume the complete response');
  output = response(result.response.statusCode, result.response.body.toString('utf8'));
} else if (name === 'http-message-parser-ts') {
  const { HttpMessageParser } = await import(name);
  const result = new HttpMessageParser().parseResponse(string);
  output = response(result.statusCode, result.body);
} else if (['@perseveranza-pets/milo', '@perseveranza-pets/milo-cjs'].includes(name)) {
  const { setup } = await import(name);
  let view, method, target;
  const milo = setup({
    on_method(_parser, offset, size) { method = view.subarray(offset, offset + size).toString('utf8'); },
    on_url(_parser, offset, size) { target = view.subarray(offset, offset + size).toString('utf8'); }
  });
  const parser = milo.create();
  milo.setActiveCallbacks(parser, milo.CALLBACK_ACTIVE_ON_METHOD | milo.CALLBACK_ACTIVE_ON_URL);
  const ptr = milo.alloc(bytes.length);
  view = Buffer.from(milo.memory.buffer, ptr, bytes.length);
  view.set(bytes);
  const used = milo.parse(parser, ptr, bytes.length);
  milo.destroy(parser);
  milo.dealloc(ptr, bytes.length);
  if (used !== bytes.length) throw new Error(`${name} did not consume the complete request`);
  output = request(method, target);
} else if (name === '@sylphx/gust-core') {
  const { initWasm } = await import(name);
  const wasm = await initWasm();
  const result = wasm.parse_http(bytes);
  const target = bytes.subarray(result.path_start, result.path_end).toString('utf8') +
    (result.query_end > result.query_start ? `?${bytes.subarray(result.query_start, result.query_end).toString('utf8')}` : '');
  output = request(wasm.method_to_string(result.method), target);
  result.free();
} else if (name === '@alikia/http-parser') {
  const { HttpParser } = await import(name);
  const messages = new HttpParser().parse(bytes);
  if (messages.length !== 1 || !messages[0].complete) throw new Error('alikia did not complete one request');
  output = request(messages[0].method, messages[0].target);
} else {
  throw new Error(`unsupported package: ${name}`);
}
if (Object.values(output).some((value) => value === undefined || value === null)) throw new Error(`${name} returned missing parsed fields`);
console.log(JSON.stringify(output));
