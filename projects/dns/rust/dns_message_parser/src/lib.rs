use bytes::Bytes;
use dns_message_parser::Dns;
use dns_message_parser::rr::{RR, ToType};
use serde_json::{Value, json};
use std::error::Error;

fn absolute(name: String) -> String {
    let lower = name.to_lowercase();
    if lower.ends_with('.') { lower } else { format!("{lower}.") }
}

/// TXT character-strings as `"<string>"` separated by spaces, the form the other DNS
/// harnesses print.
fn quoted<T: AsRef<[u8]>>(items: impl IntoIterator<Item = T>) -> String {
    items.into_iter().map(|item| format!("\"{}\"", String::from_utf8_lossy(item.as_ref())))
        .collect::<Vec<_>>().join(" ")
}

/// dns-message-parser decodes each record into a typed struct. A and AAAA records have
/// no class field because the decoder accepts them only in class IN (other classes are
/// a decode error), so the harness reports class 1 for them.
fn record(rr: &RR) -> Result<Value, Box<dyn Error>> {
    let (name, class, ttl, rdata) = match rr {
        RR::A(a) => (&a.domain_name, 1u16, a.ttl, a.ipv4_addr.to_string()),
        RR::AAAA(aaaa) => (&aaaa.domain_name, 1u16, aaaa.ttl, aaaa.ipv6_addr.to_string()),
        RR::CNAME(cname) => (&cname.domain_name, cname.class as u16, cname.ttl, absolute(cname.c_name.to_string())),
        RR::NS(ns) => (&ns.domain_name, ns.class as u16, ns.ttl, absolute(ns.ns_d_name.to_string())),
        RR::PTR(ptr) => (&ptr.domain_name, ptr.class as u16, ptr.ttl, absolute(ptr.ptr_d_name.to_string())),
        RR::MX(mx) => (&mx.domain_name, mx.class as u16, mx.ttl,
                       format!("{} {}", mx.preference, absolute(mx.exchange.to_string()))),
        RR::TXT(txt) => (&txt.domain_name, txt.class as u16, txt.ttl, quoted(txt.strings.iter())),
        other => return Err(format!("record {other} is outside the control subset").into()),
    };
    let rtype = match rr {
        RR::A(a) => a.to_type(),
        RR::AAAA(aaaa) => aaaa.to_type(),
        RR::CNAME(cname) => cname.to_type(),
        RR::NS(ns) => ns.to_type(),
        RR::PTR(ptr) => ptr.to_type(),
        RR::MX(mx) => mx.to_type(),
        RR::TXT(txt) => txt.to_type(),
        _ => unreachable!(),
    };
    Ok(json!({"name": absolute(name.to_string()), "type": rtype as u16, "class": class,
              "ttl": ttl, "rdata": rdata}))
}

fn records(list: &[RR]) -> Result<Vec<Value>, Box<dyn Error>> {
    list.iter().map(record).collect()
}

/// Decode one local DNS message with dns-message-parser's documented Dns::decode.
/// Flags keep AD and CD but not the reserved Z bit, so `z` carries AD and CD only.
pub fn parse(data: &[u8]) -> Result<Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > 65535 {
        return Err("input outside harness limit".into());
    }
    let dns = Dns::decode(Bytes::copy_from_slice(data))?;
    let questions: Vec<Value> = dns
        .questions
        .iter()
        .map(|query| json!({"name": absolute(query.domain_name.to_string()),
                            "type": query.q_type as u16, "class": query.q_class as u16}))
        .collect();
    let answers = records(&dns.answers)?;
    let authority = records(&dns.authorities)?;
    let additional = records(&dns.additionals)?;
    let flags = &dns.flags;
    let bit = |value: bool| u8::from(value);
    Ok(json!({
        "id": dns.id,
        "qr": bit(flags.qr),
        "opcode": flags.opcode as u8,
        "aa": bit(flags.aa), "tc": bit(flags.tc),
        "rd": bit(flags.rd), "ra": bit(flags.ra),
        "z": (bit(flags.ad) << 1) | bit(flags.cd),
        "rcode": flags.rcode as u8,
        "qdcount": questions.len(), "ancount": answers.len(),
        "nscount": authority.len(), "arcount": additional.len(),
        "questions": questions, "answers": answers, "authority": authority, "additional": additional,
    }))
}
