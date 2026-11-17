// Local DNS message bytes reach the documented dns2 Packet.parse(buffer) API.
const { Packet } = require('dns2');

function absolute(name) {
  const lower = String(name).toLowerCase();
  return lower === '' ? '.' : (lower.endsWith('.') ? lower : `${lower}.`);
}

function rdata(record) {
  switch (record.type) {
    case Packet.TYPE.A:
    case Packet.TYPE.AAAA:
      return record.address;  // dotted quad and compressed IPv6 text from dns2's own decoders
    case Packet.TYPE.CNAME:
    case Packet.TYPE.PTR:
      return absolute(record.domain);
    case Packet.TYPE.NS:
      return absolute(record.ns);
    case Packet.TYPE.MX:
      return `${record.priority} ${absolute(record.exchange)}`;
    case Packet.TYPE.TXT:
      return record.data.map(item => `"${item}"`).join(' ');
    default:
      return Buffer.isBuffer(record.data) ? record.data.toString('hex') : String(record.data);
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
  if (packet.errors.length) throw packet.errors[0];  // per-record decode failures are not summarised
  const header = packet.header;
  const questions = packet.questions.map(question => ({
    name: absolute(question.name), type: question.type, class: question.class,
  }));
  const answers = records(packet.answers);
  const authority = records(packet.authorities);
  const additional = records(packet.additionals);
  return {
    id: header.id, qr: header.qr, opcode: header.opcode, aa: header.aa, tc: header.tc, rd: header.rd,
    ra: header.ra, z: (header.z << 2) | (header.ad << 1) | header.cd, rcode: header.rcode,
    qdcount: questions.length, ancount: answers.length, nscount: authority.length, arcount: additional.length,
    questions, answers, authority, additional,
  };
}

module.exports = { parseData };
