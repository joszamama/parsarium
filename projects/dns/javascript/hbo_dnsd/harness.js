// Local DNS message bytes reach the documented dnsd parse(buffer) API (hbo-dnsd package).
const dnsd = require('hbo-dnsd');
const constants = require('hbo-dnsd/constants');

// dnsd's own opcode name table (message.js), read back to the opcode number.
const OPCODES = ['query', 'iquery', 'status', null, 'notify', 'update'];

function absolute(name) {
  const lower = String(name).toLowerCase();
  return lower === '' ? '.' : (lower.endsWith('.') ? lower : `${lower}.`);
}

// dnsd prints AAAA as eight zero-padded hex groups; the harness only applies RFC 5952
// leading-zero removal and zero compression to those decoded groups.
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
    case 'A': return record.data;
    case 'AAAA': return rfc5952(record.data);
    case 'CNAME': case 'NS': case 'PTR': return absolute(record.data);
    case 'MX': return `${record.data[0]} ${absolute(record.data[1])}`;
    case 'TXT': return [].concat(record.data).map(item => `"${item}"`).join(' ');
    default: return Buffer.isBuffer(record.data) ? record.data.toString('hex') : JSON.stringify(record.data);
  }
}

function records(list, question) {
  return (list || []).map(record => {
    const out = {
      name: absolute(record.name), type: constants.type_to_number(record.type),
      class: constants.class_to_number(record.class),
    };
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
  const message = dnsd.parse(data);
  const questions = records(message.question, true);
  const answers = records(message.answer, false);
  const authority = records(message.authority, false);
  const additional = records(message.additional, false);
  const opcode = OPCODES.indexOf(message.opcode);
  return {
    id: message.id, qr: message.type === 'response' ? 1 : 0, opcode: opcode < 0 ? null : opcode,
    aa: message.authoritative ? 1 : 0, tc: message.truncated ? 1 : 0, rd: message.recursion_desired ? 1 : 0,
    ra: message.recursion_available ? 1 : 0,
    // dnsd decodes AD and CD but not the reserved Z bit.
    z: ((message.authenticated ? 1 : 0) << 1) | (message.checking_disabled ? 1 : 0),
    rcode: message.responseCode,
    qdcount: questions.length, ancount: answers.length, nscount: authority.length, arcount: additional.length,
    questions, answers, authority, additional,
  };
}

module.exports = { parseData };
