// Local DNS message bytes reach the documented @portable/dns-packet decode(bytes) API.
const DnsPacket = require('@portable/dns-packet');
// The package names types, classes, opcodes and rcodes; its own code tables (dist/codes.js, not in
// the export map, loaded by file path) map those names back to numbers.
const { types, classes, opcodes, rcodes } = require('/work/node_modules/@portable/dns-packet/dist/codes.js');

function absolute(name) {
  const lower = String(name).toLowerCase();
  return lower === '' || lower === '.' ? '.' : (lower.endsWith('.') ? lower : `${lower}.`);
}

function rdata(record) {
  switch (record.type) {
    case 'A': case 'AAAA': return record.data;  // address text from the package's own codecs
    case 'CNAME': case 'NS': case 'PTR': return absolute(record.data);
    case 'MX': return `${record.data.preference} ${absolute(record.data.exchange)}`;
    case 'TXT': return record.data.map(item => `"${Buffer.from(item).toString('latin1')}"`).join(' ');
    default: return record.data instanceof Uint8Array ? Buffer.from(record.data).toString('hex') : JSON.stringify(record.data);
  }
}

function records(list, question) {
  return (list || []).map(record => {
    const out = { name: absolute(record.name), type: types.value(record.type), class: classes.value(record.class) };
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
  const packet = DnsPacket.decode(new Uint8Array(data));
  const flags = packet.flags;
  const questions = records(packet.questions, true);
  const answers = records(packet.answers, false);
  const authority = records(packet.authorities, false);
  const additional = records(packet.additionals, false);
  return {
    id: packet.id, qr: packet.type === 'response' ? 1 : 0, opcode: opcodes.value(packet.opcode),
    aa: flags.aa ? 1 : 0, tc: flags.tc ? 1 : 0, rd: flags.rd ? 1 : 0, ra: flags.ra ? 1 : 0,
    // @portable/dns-packet decodes AD and CD but not the reserved Z bit.
    z: ((flags.ad ? 1 : 0) << 1) | (flags.cd ? 1 : 0),
    rcode: rcodes.value(packet.rcode),
    qdcount: questions.length, ancount: answers.length, nscount: authority.length, arcount: additional.length,
    questions, answers, authority, additional,
  };
}

module.exports = { parseData };
