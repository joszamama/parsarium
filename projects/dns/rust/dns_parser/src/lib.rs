use dns_parser::{Packet, RData, ResourceRecord};
use serde_json::{Value, json};
use std::error::Error;

fn absolute(name: String) -> String {
    let lower = name.to_lowercase();
    if lower.ends_with('.') { lower } else { format!("{lower}.") }
}

/// dns-parser's ResourceRecord carries no numeric type field; the decoded RData variant
/// selects it, so the harness maps the variant to its RFC 1035/3596 type number.
/// TXT character-strings as `"<string>"` separated by spaces, the form the other DNS
/// harnesses print.
fn quoted<T: AsRef<[u8]>>(items: impl IntoIterator<Item = T>) -> String {
    items.into_iter().map(|item| format!("\"{}\"", String::from_utf8_lossy(item.as_ref())))
        .collect::<Vec<_>>().join(" ")
}

fn rdata(record: &ResourceRecord) -> Result<(u16, String), Box<dyn Error>> {
    Ok(match &record.data {
        RData::A(a) => (1, a.0.to_string()),
        RData::AAAA(aaaa) => (28, aaaa.0.to_string()),
        RData::CNAME(cname) => (5, absolute(cname.0.to_string())),
        RData::NS(ns) => (2, absolute(ns.0.to_string())),
        RData::PTR(ptr) => (12, absolute(ptr.0.to_string())),
        RData::MX(mx) => (15, format!("{} {}", mx.preference, absolute(mx.exchange.to_string()))),
        RData::TXT(txt) => (16, quoted(txt.iter())),
        _ => return Err("record data outside the control subset".into()),
    })
}

fn records(list: &[ResourceRecord]) -> Result<Vec<Value>, Box<dyn Error>> {
    list.iter()
        .map(|record| {
            let (rtype, text) = rdata(record)?;
            Ok(json!({"name": absolute(record.name.to_string()), "type": rtype,
                      "class": record.cls as u16, "ttl": record.ttl, "rdata": text}))
        })
        .collect()
}

/// Decode one local DNS message with dns-parser's documented Packet::parse.
/// The header keeps AD and CD but not the reserved Z bit, so `z` carries AD and CD only.
pub fn parse(data: &[u8]) -> Result<Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > 65535 {
        return Err("input outside harness limit".into());
    }
    let packet = Packet::parse(data)?;
    let questions: Vec<Value> = packet
        .questions
        .iter()
        .map(|query| json!({"name": absolute(query.qname.to_string()),
                            "type": query.qtype as u16, "class": query.qclass as u16}))
        .collect();
    let answers = records(&packet.answers)?;
    let authority = records(&packet.nameservers)?;
    let additional = records(&packet.additional)?;
    let header = &packet.header;
    let bit = |value: bool| u8::from(value);
    let opcode: u16 = header.opcode.into();
    let rcode: u8 = header.response_code.into();
    Ok(json!({
        "id": header.id,
        "qr": bit(!header.query),
        "opcode": opcode,
        "aa": bit(header.authoritative), "tc": bit(header.truncated),
        "rd": bit(header.recursion_desired), "ra": bit(header.recursion_available),
        "z": (bit(header.authenticated_data) << 1) | bit(header.checking_disabled),
        "rcode": rcode,
        "qdcount": questions.len(), "ancount": answers.len(),
        "nscount": authority.len(), "arcount": additional.len(),
        "questions": questions, "answers": answers, "authority": authority, "additional": additional,
    }))
}
