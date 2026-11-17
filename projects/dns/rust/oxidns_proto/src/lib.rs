use oxidns_proto::{MessageType, Message, RData, Record};
use serde_json::{Value, json};
use std::error::Error;

/// oxidns-proto's Name::to_fqdn() is the canonical (lower-case) name with the trailing dot.
fn rdata(record: &Record) -> Result<String, Box<dyn Error>> {
    Ok(match record.data() {
        RData::A(address) => address.0.to_string(),
        RData::AAAA(address) => address.0.to_string(),
        RData::CNAME(target) => target.0.to_fqdn(),
        RData::NS(target) => target.0.to_fqdn(),
        RData::PTR(target) => target.0.to_fqdn(),
        RData::MX(mx) => format!("{} {}", mx.preference(), mx.exchange().to_fqdn()),
        _ => return Err(format!("record type {} is outside the control subset", u16::from(record.rr_type())).into()),
    })
}

fn records(list: &[Record]) -> Result<Vec<Value>, Box<dyn Error>> {
    list.iter()
        .map(|record| {
            Ok(json!({"name": record.name().to_fqdn(), "type": u16::from(record.rr_type()),
                      "class": u16::from(record.class()), "ttl": record.ttl(), "rdata": rdata(record)?}))
        })
        .collect()
}

/// Decode one local DNS message with oxidns-proto's documented Message::from_bytes.
/// The header keeps AD and CD but not the reserved Z bit, so `z` carries AD and CD only.
pub fn parse(data: &[u8]) -> Result<Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > 65535 {
        return Err("input outside harness limit".into());
    }
    let message = Message::from_bytes(data)?;
    let questions: Vec<Value> = message
        .questions()
        .iter()
        .map(|question| json!({"name": question.name().to_fqdn(),
                               "type": u16::from(question.qtype()),
                               "class": u16::from(question.qclass())}))
        .collect();
    let answers = records(message.answers())?;
    let authority = records(message.authorities())?;
    let additional = records(message.additionals())?;
    Ok(json!({
        "id": message.id(),
        "qr": u8::from(message.message_type() == MessageType::Response),
        "opcode": u8::from(message.opcode()),
        "aa": u8::from(message.authoritative()), "tc": u8::from(message.truncated()),
        "rd": u8::from(message.recursion_desired()), "ra": u8::from(message.recursion_available()),
        "z": (u8::from(message.authentic_data()) << 1) | u8::from(message.checking_disabled()),
        "rcode": u16::from(message.rcode()),
        "qdcount": message.question_count(), "ancount": message.answer_count(),
        "nscount": message.authority_count(), "arcount": message.additional_count(),
        "questions": questions, "answers": answers, "authority": authority, "additional": additional,
    }))
}
