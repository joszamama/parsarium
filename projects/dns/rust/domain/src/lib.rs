use domain::base::name::ParsedName;
use domain::base::{Message, RecordSection};
use domain::rdata::AllRecordData;
use serde_json::{Value, json};
use std::error::Error;

type Parsed<'a> = ParsedName<&'a [u8]>;

fn absolute(name: String) -> String {
    let lower = name.to_lowercase();
    if lower.ends_with('.') { lower } else { format!("{lower}.") }
}

fn rdata(data: &AllRecordData<&[u8], Parsed>) -> Result<String, Box<dyn Error>> {
    Ok(match data {
        AllRecordData::A(a) => a.addr().to_string(),
        AllRecordData::Aaaa(aaaa) => aaaa.addr().to_string(),
        AllRecordData::Cname(cname) => absolute(cname.cname().to_string()),
        AllRecordData::Ns(ns) => absolute(ns.nsdname().to_string()),
        AllRecordData::Ptr(ptr) => absolute(ptr.ptrdname().to_string()),
        AllRecordData::Mx(mx) => format!("{} {}", mx.preference(), absolute(mx.exchange().to_string())),
        other => return Err(format!("record data {other:?} is outside the control subset").into()),
    })
}

fn records(section: RecordSection<'_, [u8]>) -> Result<Vec<Value>, Box<dyn Error>> {
    let mut out = Vec::new();
    for record in section.into_records::<AllRecordData<&[u8], Parsed>>() {
        let record = record?;
        out.push(json!({"name": absolute(record.owner().to_string()),
                        "type": record.rtype().to_int(),
                        "class": record.class().to_int(),
                        "ttl": record.ttl().as_secs(), "rdata": rdata(record.data())?}));
    }
    Ok(out)
}

/// Decode one local DNS message with domain's documented Message::from_slice, then
/// walk the question and record sections. domain keeps the Z, AD and CD bits.
pub fn parse(data: &[u8]) -> Result<Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > 65535 {
        return Err("input outside harness limit".into());
    }
    let message = Message::from_slice(data).map_err(|error| format!("{error}"))?;
    let mut questions = Vec::new();
    for question in message.question() {
        let question = question?;
        questions.push(json!({"name": absolute(question.qname().to_string()),
                              "type": question.qtype().to_int(),
                              "class": question.qclass().to_int()}));
    }
    let answers = records(message.answer()?)?;
    let authority = records(message.authority()?)?;
    let additional = records(message.additional()?)?;
    let header = message.header();
    let bit = |value: bool| u8::from(value);
    Ok(json!({
        "id": header.id(),
        "qr": bit(header.qr()),
        "opcode": header.opcode().to_int(),
        "aa": bit(header.aa()), "tc": bit(header.tc()),
        "rd": bit(header.rd()), "ra": bit(header.ra()),
        "z": (bit(header.z()) << 2) | (bit(header.ad()) << 1) | bit(header.cd()),
        "rcode": header.rcode().to_int(),
        "qdcount": questions.len(), "ancount": answers.len(),
        "nscount": authority.len(), "arcount": additional.len(),
        "questions": questions, "answers": answers, "authority": authority, "additional": additional,
    }))
}
