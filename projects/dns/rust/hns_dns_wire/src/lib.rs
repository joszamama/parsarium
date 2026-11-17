use hns_dns_wire::{Message, Rdata, ResourceRecord};
use serde_json::{Value, json};
use std::error::Error;

/// hns-dns-wire prints names lower case and absolute (with the trailing dot) and keeps
/// A/AAAA as std::net addresses; the harness only joins MX as "<preference> <exchange>".
fn rdata(record: &ResourceRecord) -> Result<String, Box<dyn Error>> {
    Ok(match &record.rdata {
        Rdata::A(address) => address.to_string(),
        Rdata::Aaaa(address) => address.to_string(),
        Rdata::Cname(target) | Rdata::Ns(target) => target.to_string(),
        Rdata::Mx(mx) => format!("{} {}", mx.preference, mx.exchange),
        _ => return Err(format!("record type {} is outside the control subset", record.record_type.code()).into()),
    })
}

fn records(list: &[ResourceRecord]) -> Result<Vec<Value>, Box<dyn Error>> {
    list.iter()
        .map(|record| {
            Ok(json!({"name": record.name.to_string(), "type": record.record_type.code(),
                      "class": record.class, "ttl": record.ttl, "rdata": rdata(record)?}))
        })
        .collect()
}

/// Decode one local DNS message with hns-dns-wire's documented Message::parse.
/// The library rejects a set reserved Z bit and has an accessor for AD but not CD, so `z`
/// is read as the three bits after RA of the parsed Flags::bits() word.
pub fn parse(data: &[u8]) -> Result<Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > 65535 {
        return Err("input outside harness limit".into());
    }
    let message = Message::parse(data)?;
    let flags = message.header.flags;
    let questions: Vec<Value> = message
        .questions
        .iter()
        .map(|question| json!({"name": question.name.to_string(),
                               "type": question.record_type.code(), "class": question.class}))
        .collect();
    let answers = records(&message.answers)?;
    let authority = records(&message.authorities)?;
    let additional = records(&message.additionals)?;
    Ok(json!({
        "id": message.header.id,
        "qr": u8::from(flags.is_response()), "opcode": flags.opcode(),
        "aa": u8::from(flags.authoritative()), "tc": u8::from(flags.truncated()),
        "rd": u8::from(flags.recursion_desired()), "ra": u8::from(flags.recursion_available()),
        "z": (flags.bits() >> 4) & 0x7, "rcode": flags.rcode(),
        "qdcount": message.header.question_count, "ancount": message.header.answer_count,
        "nscount": message.header.authority_count, "arcount": message.header.additional_count,
        "questions": questions, "answers": answers, "authority": authority, "additional": additional,
    }))
}
