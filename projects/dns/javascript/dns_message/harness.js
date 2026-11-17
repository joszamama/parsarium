// Local DNS message bytes reach the documented dns-message decode(bytes) API.
const { decode, RecordType } = require('dns-message');

function absolute(name) {
  const lower = String(name).toLowerCase();
  return lower === '' || lower === '.' ? '.' : (lower.endsWith('.') ? lower : `${lower}.`);
}

function rdata(record) {
  switch (record.type) {
    case RecordType.A: case RecordType.AAAA: return record.data;  // address text from dns-message's own codecs
    case RecordType.CNAME: case RecordType.NS: case RecordType.PTR: return absolute(record.data);
    case RecordType.MX: return `${record.data.preference} ${absolute(record.data.exchange)}`;
    case RecordType.TXT: return [].concat(record.data).map(item => `"${typeof item === 'string' ? item : Buffer.from(item).toString('latin1')}"`).join(' ');
    default: return record.data instanceof Uint8Array ? Buffer.from(record.data).toString('hex') : JSON.stringify(record.data);
  }
}

function records(list, question) {
  return (list || []).map(record => {
    const out = { name: absolute(record.name), type: record.type, class: record.class };
    if (!question) Object.assign(out, { ttl: record.ttl, rdata: rdata(record) });
    return out;
  });
}

function parseData(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > 65535) {
    const rejected = new Error('input outside harness limit');
    rejected.name = 'InputLimitError';
    throw rejected;
  }
  const packet = decode(new Uint8Array(data));
  const flags = packet.flags;  // the 16-bit flags word as decoded by dns-message
  const questions = records(packet.questions, true);
  const answers = records(packet.answers, false);
  const authority = records(packet.authorities, false);
  const additional = records(packet.additionals, false);
  return {
    id: packet.id, qr: (flags >> 15) & 1, opcode: (flags >> 11) & 15, aa: (flags >> 10) & 1, tc: (flags >> 9) & 1,
    rd: (flags >> 8) & 1, ra: (flags >> 7) & 1, z: (flags >> 4) & 7, rcode: packet.rtype,
    qdcount: questions.length, ancount: answers.length, nscount: authority.length, arcount: additional.length,
    questions, answers, authority, additional,
  };
}

module.exports = { parseData };
