// Local DNS message bytes reach the documented native-dns-packet Packet.parse(buffer) API.
const Packet = require('native-dns-packet');
const { NAME_TO_QTYPE: TYPE } = Packet.consts;

function absolute(name) {
  const lower = String(name).toLowerCase();
  return lower === '' ? '.' : (lower.endsWith('.') ? lower : `${lower}.`);
}

// native-dns-packet prints AAAA as eight uncompressed hex groups; the harness only applies
// RFC 5952 zero compression to those decoded groups.
function rfc5952(groups) {
  const parts = groups.split(':').map(group => parseInt(group, 16).toString(16));
  let bestStart = -1, bestLength = 0;
  for (let i = 0; i < parts.length;) {
    if (parts[i] !== '0') { i++; continue; }
    let j = i;
    while (j < parts.length && parts[j] === '0') j++;
    if (j - i > bestLength) { bestStart = i; bestLength = j - i; }
    i = j;
  }
  if (bestLength < 2) return parts.join(':');
  return `${parts.slice(0, bestStart).join(':')}::${parts.slice(bestStart + bestLength).join(':')}`;
}

function rdata(record) {
  switch (record.type) {
    case TYPE.A: return record.address;
    case TYPE.AAAA: return rfc5952(record.address);
    case TYPE.CNAME: case TYPE.NS: case TYPE.PTR: return absolute(record.data);
    case TYPE.MX: return `${record.priority} ${absolute(record.exchange)}`;
    case TYPE.TXT: return record.data.map(item => `"${item}"`).join(' ');
    default: return Buffer.isBuffer(record.data) ? record.data.toString('hex') : String(record.data);
  }
}

function records(list) {
  return (list || []).map(record => ({
    name: absolute(record.name), type: record.type, class: record.class, ttl: record.ttl, rdata: rdata(record),
  }));
}

function parseData(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > 65535) {
    const rejected = new Error('input outside harness limit');
    rejected.name = 'InputLimitError';
    throw rejected;
  }
  const packet = Packet.parse(data);
  const header = packet.header;
  const questions = packet.question.map(question => ({
    name: absolute(question.name), type: question.type, class: question.class,
  }));
  const answers = records(packet.answer);
  const authority = records(packet.authority);
  const additional = records(packet.additional);
  return {
    id: header.id, qr: header.qr, opcode: header.opcode, aa: header.aa, tc: header.tc, rd: header.rd,
    ra: header.ra, z: (header.res1 << 2) | (header.res2 << 1) | header.res3, rcode: header.rcode,
    qdcount: questions.length, ancount: answers.length, nscount: authority.length, arcount: additional.length,
    questions, answers, authority, additional,
  };
}

module.exports = { parseData };
