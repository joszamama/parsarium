use hickory_proto::op::{Message, MessageType};
use hickory_proto::rr::{RData, Record};
use serde_json::{Value, json};
use std::error::Error;

fn absolute(name: String) -> String {
    let lower = name.to_lowercase();
    if lower.ends_with('.') { lower } else { format!("{lower}.") }
}

fn rdata(record: &Record) -> Result<String, Box<dyn Error>> {
    Ok(match &record.data {
        RData::A(address) => address.0.to_string(),
        RData::AAAA(address) => address.0.to_string(),
        RData::CNAME(target) => absolute(target.0.to_string()),
        RData::NS(target) => absolute(target.0.to_string()),
        RData::PTR(target) => absolute(target.0.to_string()),
        RData::MX(mx) => format!("{} {}", mx.preference, absolute(mx.exchange.to_string())),
        RData::TXT(txt) => txt
            .txt_data
            .iter()
            .map(|item| format!("\"{}\"", String::from_utf8_lossy(item)))
            .collect::<Vec<_>>()
            .join(" "),
        other => return Err(format!("record type {:?} is outside the control subset", other.record_type()).into()),
    })
}

fn records(list: &[Record]) -> Result<Vec<Value>, Box<dyn Error>> {
    list.iter()
        .map(|record| {
            Ok(json!({"name": absolute(record.name.to_string()),
                      "type": u16::from(record.record_type()),
                      "class": u16::from(record.dns_class),
                      "ttl": record.ttl, "rdata": rdata(record)?}))
        })
        .collect()
}

/// Decode one local DNS message with hickory-proto's documented Message::from_vec.
/// hickory-proto keeps AD and CD but not the reserved Z bit, so `z` carries AD and CD only.
pub fn parse(data: &[u8]) -> Result<Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > 65535 {
        return Err("input outside harness limit".into());
    }
    let message = Message::from_vec(data)?;
    let questions: Vec<Value> = message
        .queries
        .iter()
        .map(|query| json!({"name": absolute(query.name.to_string()),
                            "type": u16::from(query.query_type),
                            "class": u16::from(query.query_class)}))
        .collect();
    let answers = records(&message.answers)?;
    let authority = records(&message.authorities)?;
    let additional = records(&message.additionals)?;
    let bit = |value: bool| u8::from(value);
    let meta = &message.metadata;
    Ok(json!({
        "id": meta.id,
        "qr": bit(meta.message_type == MessageType::Response),
        "opcode": u8::from(meta.op_code),
        "aa": bit(meta.authoritative), "tc": bit(meta.truncation),
        "rd": bit(meta.recursion_desired), "ra": bit(meta.recursion_available),
        "z": (bit(meta.authentic_data) << 1) | bit(meta.checking_disabled),
        "rcode": u16::from(meta.response_code),
        "qdcount": questions.len(), "ancount": answers.len(),
        "nscount": authority.len(), "arcount": additional.len(),
        "questions": questions, "answers": answers, "authority": authority, "additional": additional,
    }))
}
