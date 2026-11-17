use rsdns::message::reader::MessageIterator;
use rsdns::message::{MessageType, RecordsSection};
use rsdns::records::ResourceRecord;
use rsdns::records::data::RecordData;
use serde_json::{Value, json};
use std::error::Error;

fn absolute(name: String) -> String {
    let lower = name.to_lowercase();
    if lower.ends_with('.') { lower } else { format!("{lower}.") }
}

fn rdata(record: &ResourceRecord) -> Result<String, Box<dyn Error>> {
    Ok(match &record.rdata {
        RecordData::A(a) => a.address.to_string(),
        RecordData::Aaaa(aaaa) => aaaa.address.to_string(),
        RecordData::Cname(cname) => absolute(cname.cname.to_string()),
        RecordData::Ns(ns) => absolute(ns.nsdname.to_string()),
        RecordData::Ptr(ptr) => absolute(ptr.ptrdname.to_string()),
        RecordData::Mx(mx) => format!("{} {}", mx.preference, absolute(mx.exchange.to_string())),
        _ => return Err("record data outside the control subset".into()),
    })
}

/// Decode one local DNS message with rsdns's documented MessageIterator::new, then read
/// its questions and records (each tagged with its section) through the iterator.
/// rsdns exposes no Z, AD or CD flag, so `z` is reported as 0.
pub fn parse(data: &[u8]) -> Result<Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > 65535 {
        return Err("input outside harness limit".into());
    }
    let message = MessageIterator::new(data)?;
    let mut questions = Vec::new();
    for question in message.questions() {
        let question = question?;
        questions.push(json!({"name": absolute(question.qname.to_string()),
                              "type": question.qtype.value(), "class": question.qclass.value()}));
    }
    let (mut answers, mut authority, mut additional) = (Vec::new(), Vec::new(), Vec::new());
    for item in message.records() {
        let (section, record) = item?;
        let value = json!({"name": absolute(record.name.to_string()), "type": record.rtype.value(),
                           "class": record.rclass.value(), "ttl": record.ttl, "rdata": rdata(&record)?});
        match section {
            RecordsSection::Answer => answers.push(value),
            RecordsSection::Authority => authority.push(value),
            RecordsSection::Additional => additional.push(value),
        }
    }
    let header = message.header();
    let flags = header.flags;
    let bit = |value: bool| u8::from(value);
    Ok(json!({
        "id": header.id,
        "qr": bit(flags.message_type() == MessageType::Response),
        "opcode": flags.opcode().value(),
        "aa": bit(flags.authoritative_answer()), "tc": bit(flags.truncated()),
        "rd": bit(flags.recursion_desired()), "ra": bit(flags.recursion_available()),
        "z": 0,
        "rcode": flags.response_code().value(),
        "qdcount": questions.len(), "ancount": answers.len(),
        "nscount": authority.len(), "arcount": additional.len(),
        "questions": questions, "answers": answers, "authority": authority, "additional": additional,
    }))
}
