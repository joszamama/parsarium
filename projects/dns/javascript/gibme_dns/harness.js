// Local DNS message bytes reach the documented @gibme/dns `new Packet(buffer)` decoder.
const { Packet, RType, RClass } = require('@gibme/dns');

function absolute(name) {
  const lower = String(name).toLowerCase();
  return lower === '' ? '.' : (lower.endsWith('.') ? lower : `${lower}.`);
}

// RFC 5952 leading-zero removal and zero compression applied to the hex groups of the
// address text that @gibme/dns returns (decoded through its ip-address dependency).
function rfc5952(text) {
  if (text.includes('::')) return text.toLowerCase();
  const parts = text.split(':').map(group => parseInt(group, 16).toString(16));
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
    case 'A': return record.data;
    case 'AAAA': return rfc5952(record.data);
    case 'CNAME': case 'NS': case 'PTR': return absolute(record.data);
    case 'MX': return `${record.data.preference} ${absolute(record.data.exchange)}`;
    case 'TXT': return record.data.map(item => `"${item}"`).join(' ');
    default: return JSON.stringify(record.data);
  }
}

function records(list, question) {
  return (list || []).map(record => {
    const out = { name: absolute(record.name), type: new RType(record.type).id, class: new RClass(record.class).id };
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
  const packet = new Packet(data);
  const questions = records(packet.questions, true);
  const answers = records(packet.answers, false);
  const authority = records(packet.authorities, false);
  const additional = records(packet.additionals, false);
  return {
    id: packet.id, qr: packet.type, opcode: packet.opcode, aa: packet.authoritative_answer ? 1 : 0,
    tc: packet.truncated ? 1 : 0, rd: packet.recursion_desired ? 1 : 0, ra: packet.recursion_available ? 1 : 0,
    z: ((packet.z ? 1 : 0) << 2) | ((packet.authentic_data ? 1 : 0) << 1) | (packet.checking_disabled ? 1 : 0),
    rcode: packet.rcode,
    qdcount: questions.length, ancount: answers.length, nscount: authority.length, arcount: additional.length,
    questions, answers, authority, additional,
  };
}

module.exports = { parseData };
