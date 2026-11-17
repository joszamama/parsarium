use serde_json::{Value, json};
use simple_dns::rdata::RData;
use simple_dns::{Packet, PacketFlag, ResourceRecord};
use std::error::Error;
use std::net::{Ipv4Addr, Ipv6Addr};

fn absolute(name: String) -> String {
    let lower = name.to_lowercase();
    if lower.ends_with('.') { lower } else { format!("{lower}.") }
}

/// simple-dns stores A and AAAA addresses as u32/u128 integers; the harness prints them
/// with std::net (dotted quad, RFC 5952).
fn rdata(record: &ResourceRecord) -> Result<String, Box<dyn Error>> {
    Ok(match &record.rdata {
        RData::A(address) => Ipv4Addr::from(address.address).to_string(),
        RData::AAAA(address) => Ipv6Addr::from(address.address).to_string(),
        RData::CNAME(target) => absolute(target.0.to_string()),
        RData::NS(target) => absolute(target.0.to_string()),
        RData::PTR(target) => absolute(target.0.to_string()),
        RData::MX(mx) => format!("{} {}", mx.preference, absolute(mx.exchange.to_string())),
        other => return Err(format!("record type {} is outside the control subset", u16::from(other.type_code())).into()),
    })
}

fn records(list: &[ResourceRecord]) -> Result<Vec<Value>, Box<dyn Error>> {
    list.iter()
        .map(|record| {
            Ok(json!({"name": absolute(record.name.to_string()),
                      "type": u16::from(record.rdata.type_code()),
                      "class": u16::from(record.class),
                      "ttl": record.ttl, "rdata": rdata(record)?}))
        })
        .collect()
}

/// Decode one local DNS message with simple-dns's documented Packet::parse.
/// simple-dns keeps AD and CD as packet flags but not the reserved Z bit, so `z` carries AD and CD only.
pub fn parse(data: &[u8]) -> Result<Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > 65535 {
        return Err("input outside harness limit".into());
    }
    let packet = Packet::parse(data)?;
    let questions: Vec<Value> = packet
        .questions
        .iter()
        .map(|query| json!({"name": absolute(query.qname.to_string()),
                            "type": u16::from(query.qtype),
                            "class": u16::from(query.qclass)}))
        .collect();
    let answers = records(&packet.answers)?;
    let authority = records(&packet.name_servers)?;
    let additional = records(&packet.additional_records)?;
    let bit = |flag: PacketFlag| u8::from(packet.has_flags(flag));
    Ok(json!({
        "id": packet.id(),
        "qr": bit(PacketFlag::RESPONSE),
        "opcode": packet.opcode() as u16,
        "aa": bit(PacketFlag::AUTHORITATIVE_ANSWER), "tc": bit(PacketFlag::TRUNCATION),
        "rd": bit(PacketFlag::RECURSION_DESIRED), "ra": bit(PacketFlag::RECURSION_AVAILABLE),
        "z": (bit(PacketFlag::AUTHENTIC_DATA) << 1) | bit(PacketFlag::CHECKING_DISABLED),
        "rcode": packet.rcode() as u16,
        "qdcount": questions.len(), "ancount": answers.len(),
        "nscount": authority.len(), "arcount": additional.len(),
        "questions": questions, "answers": answers, "authority": authority, "additional": additional,
    }))
}
