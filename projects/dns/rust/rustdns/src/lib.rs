use rustdns::{Message, QR, Record, Resource};
use serde_json::{Value, json};
use std::error::Error;

fn absolute(name: String) -> String {
    let lower = name.to_lowercase();
    if lower.ends_with('.') { lower } else { format!("{lower}.") }
}

fn rdata(record: &Record) -> Result<String, Box<dyn Error>> {
    Ok(match &record.resource {
        Resource::A(address) => address.to_string(),
        Resource::AAAA(address) => address.to_string(),
        Resource::CNAME(target) => absolute(target.clone()),
        Resource::NS(target) => absolute(target.clone()),
        Resource::PTR(target) => absolute(target.clone()),
        Resource::MX(mx) => format!("{} {}", mx.preference, absolute(mx.exchange.clone())),
        other => return Err(format!("record {other:?} is outside the control subset").into()),
    })
}

fn records(list: &[Record]) -> Result<Vec<Value>, Box<dyn Error>> {
    list.iter()
        .map(|record| {
            Ok(json!({"name": absolute(record.name.clone()),
                      "type": record.r#type() as u16,
                      "class": record.class as u16,
                      "ttl": record.ttl.as_secs(), "rdata": rdata(record)?}))
        })
        .collect()
}

/// Decode one local DNS message with rustdns's documented Message::from_slice.
/// rustdns keeps the Z, AD and CD bits.
pub fn parse(data: &[u8]) -> Result<Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > 65535 {
        return Err("input outside harness limit".into());
    }
    let message = Message::from_slice(data)?;
    let questions: Vec<Value> = message
        .questions
        .iter()
        .map(|query| json!({"name": absolute(query.name.clone()),
                            "type": query.r#type as u16, "class": query.class as u16}))
        .collect();
    let answers = records(&message.answers)?;
    let authority = records(&message.authoritys)?;
    let additional = records(&message.additionals)?;
    let bit = |value: bool| u8::from(value);
    Ok(json!({
        "id": message.id,
        "qr": bit(message.qr == QR::Response),
        "opcode": message.opcode as u8,
        "aa": bit(message.aa), "tc": bit(message.tc),
        "rd": bit(message.rd), "ra": bit(message.ra),
        "z": (bit(message.z) << 2) | (bit(message.ad) << 1) | bit(message.cd),
        "rcode": message.rcode as u16,
        "qdcount": questions.len(), "ancount": answers.len(),
        "nscount": authority.len(), "arcount": additional.len(),
        "questions": questions, "answers": answers, "authority": authority, "additional": additional,
    }))
}
