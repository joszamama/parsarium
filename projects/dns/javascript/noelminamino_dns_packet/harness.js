// Local DNS message bytes reach the documented @noelminamino/dns-packet decode(buf) API.
const dnsPacket = require('@noelminamino/dns-packet');
const types = require('@noelminamino/dns-packet/types.js');
const classes = require('@noelminamino/dns-packet/classes.js');

function absolute(name) {
  const lower = String(name).toLowerCase();
  return lower === '' ? '.' : (lower.endsWith('.') ? lower : `${lower}.`);
}

function rdata(record) {
  if (record.type === 'MX') return `${record.data.preference} ${absolute(record.data.exchange)}`;
  if (['CNAME', 'NS', 'PTR'].includes(record.type)) return absolute(record.data);
  if (record.type === 'TXT') return record.data.map(item => `"${Buffer.from(item).toString('latin1')}"`).join(' ');
  return String(record.data);  // A and AAAA text from the package's ip-codec decoding
}

function records(list) {
  return (list || []).map(record => ({
    name: absolute(record.name), type: types.toType(record.type), class: classes.toClass(record.class),
    ttl: record.ttl, rdata: rdata(record),
  }));
}

function parseData(data) {
  if (!Buffer.isBuffer(data) || data.length === 0 || data.length > 65535) {
    const rejected = new Error('input outside harness limit');
    rejected.name = 'InputLimitError';
    throw rejected;
  }
  const packet = dnsPacket.decode(data);
  const flags = packet.flags;  // the 16-bit flags word as decoded by @noelminamino/dns-packet, QR masked off
  const questions = (packet.questions || []).map(question => ({
    name: absolute(question.name), type: types.toType(question.type), class: classes.toClass(question.class),
  }));
  const answers = records(packet.answers);
  const authority = records(packet.authorities);
  const additional = records(packet.additionals);
  return {
    id: packet.id, qr: packet.type === 'response' ? 1 : 0, opcode: (flags >> 11) & 15,
    aa: packet.flag_aa ? 1 : 0, tc: packet.flag_tc ? 1 : 0, rd: packet.flag_rd ? 1 : 0,
    ra: packet.flag_ra ? 1 : 0, z: (flags >> 4) & 7, rcode: flags & 15,
    qdcount: questions.length, ancount: answers.length, nscount: authority.length, arcount: additional.length,
    questions, answers, authority, additional,
  };
}

module.exports = { parseData };
