const { HTTPParser } = require('http-parser-js');

function parseHttp(data) {
  if (!data || data.length === 0 || data.length > (1 << 20)) {
    throw new Error('input outside harness limit');
  }
  const bytes = Buffer.from(data);
  const parser = new HTTPParser(HTTPParser.REQUEST);
  let info;
  parser[HTTPParser.kOnHeadersComplete] = value => { info = value; };
  const used = parser.execute(bytes);
  if (used instanceof Error || used !== bytes.length || !info) return null;
  return { method: HTTPParser.methods[info.method], target: info.url };
}
module.exports = { parseHttp };
