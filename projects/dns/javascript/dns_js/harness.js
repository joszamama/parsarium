// Local DNS message bytes reach the documented dns-js DNSPacket.parse(buffer) API.
const dns = require('dns-js');
const Type = dns.DNSRecord.Type;

function absolute(name) {
  const lower = String(name).toLowerCase();
  return lower === '' ? '.' : (lower.endsWith('.') ? lower : `${lower}.`);
}

// dns-js prints AAAA as eight uncompressed hex groups; the harness only applies RFC 5952
// zero compression to those decoded groups.
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
    case Type.A: return record.address;
    case Type.AAAA: return rfc5952(record.address);
    case Type.CNAME: case Type.NS: case Type.PTR: return absolute(record.data);
    case Type.MX: return `${record.priority} ${absolute(record.exchange)}`;
    case Type.TXT: return record.data.map(item => `"${item}"`).join(' ');
    default: return String(record.data);
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
  const packet = dns.DNSPacket.parse(data);
  // dns-js returns an array when bytes follow the first message; only one message is summarised.
  if (Array.isArray(packet)) throw new Error('trailing bytes after the DNS message');
  const header = packet.header;
  const questions = records(packet.question, true);
  const answers = records(packet.answer, false);
  const authority = records(packet.authority, false);
  const additional = records(packet.additional, false);
  return {
    id: header.id, qr: header.qr, opcode: header.opcode, aa: header.aa, tc: header.tc, rd: header.rd,
    ra: header.ra, z: (header.res1 << 2) | (header.res2 << 1) | header.res3, rcode: header.rcode,
    qdcount: questions.length, ancount: answers.length, nscount: authority.length, arcount: additional.length,
    questions, answers, authority, additional,
  };
}

module.exports = { parseData };
