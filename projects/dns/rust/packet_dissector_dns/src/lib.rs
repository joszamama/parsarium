use packet_dissector_core::dissector::Dissector;
use packet_dissector_core::field::{Field, FieldValue, FormatContext};
use packet_dissector_core::packet::{DissectBuffer, Layer};
use packet_dissector_dns::{DnsDissector, write_dns_name};
use serde_json::{Map, Value, json};
use std::error::Error;
use std::net::{Ipv4Addr, Ipv6Addr};

type Res<T> = Result<T, Box<dyn Error>>;

fn number(field: &Field<'_>) -> Res<u64> {
    Ok(match field.value {
        FieldValue::U8(v) => v.into(),
        FieldValue::U16(v) => v.into(),
        FieldValue::U32(v) => v.into(),
        FieldValue::U64(v) => v,
        _ => return Err(format!("field {} is not a number", field.name()).into()),
    })
}

/// Decode a name field with the dissector crate's public write_dns_name FormatFn, which
/// follows the compression pointers inside the DNS layer; the harness only adds the
/// trailing dot and lower-cases it.
fn name(data: &[u8], buf: &DissectBuffer<'_>, layer: &Layer, field: &Field<'_>) -> Res<String> {
    let ctx = FormatContext {
        packet_data: data,
        scratch: buf.scratch(),
        layer_range: layer.range.start as u32..layer.range.end as u32,
        field_range: field.range.start as u32..field.range.end as u32,
    };
    let mut out = Vec::new();
    write_dns_name(&field.value, &ctx, &mut out)?;
    let text: String = serde_json::from_slice(&out)?;
    let lower = text.to_lowercase();
    Ok(if lower.ends_with('.') { lower } else { format!("{lower}.") })
}

fn children<'a, 'pkt>(buf: &'a DissectBuffer<'pkt>, field: &Field<'pkt>) -> Res<&'a [Field<'pkt>]> {
    match &field.value {
        FieldValue::Object(range) | FieldValue::Array(range) => Ok(buf.nested_fields(range)),
        _ => Err(format!("field {} is not a container", field.name()).into()),
    }
}

/// Top-level Object entries of an Array field (nested containers are skipped).
fn entries<'a, 'pkt>(buf: &'a DissectBuffer<'pkt>, array: &Field<'pkt>) -> Res<Vec<&'a Field<'pkt>>> {
    let all = children(buf, array)?;
    let mut out = Vec::new();
    let mut i = 0;
    while i < all.len() {
        let field = &all[i];
        if let FieldValue::Object(range) = &field.value {
            out.push(field);
            i += 1 + (range.end - range.start) as usize;
        } else {
            i += 1;
        }
    }
    Ok(out)
}

fn object<'a, 'pkt>(buf: &'a DissectBuffer<'pkt>, entry: &Field<'pkt>) -> Res<Vec<(&'a str, &'a Field<'pkt>)>> {
    Ok(children(buf, entry)?.iter().map(|f| (f.name(), f)).collect())
}

fn get<'a, 'pkt>(fields: &[(&str, &'a Field<'pkt>)], key: &str) -> Res<&'a Field<'pkt>> {
    fields.iter().find(|(k, _)| *k == key).map(|(_, f)| *f).ok_or_else(|| format!("missing {key}").into())
}

fn records(data: &[u8], buf: &DissectBuffer<'_>, layer: &Layer, key: &str) -> Res<Vec<Value>> {
    let Some(array) = buf.field_by_name(layer, key) else { return Ok(vec![]) };
    let mut out = Vec::new();
    for entry in entries(buf, array)? {
        let fields = object(buf, entry)?;
        let rtype = number(get(&fields, "type")?)?;
        // A/AAAA arrive as Ipv4Addr/Ipv6Addr values, CNAME/NS/PTR as the wire name the
        // dissector validated, MX as rdata_preference + rdata_exchange.
        let rdata = match rtype {
            1 | 28 => match get(&fields, "rdata")?.value {
                FieldValue::Ipv4Addr(a) => Ipv4Addr::from(a).to_string(),
                FieldValue::Ipv6Addr(a) => Ipv6Addr::from(a).to_string(),
                _ => return Err("address rdata not decoded".into()),
            },
            2 | 5 | 12 => name(data, buf, layer, get(&fields, "rdata")?)?,
            15 => format!("{} {}", number(get(&fields, "rdata_preference")?)?,
                          name(data, buf, layer, get(&fields, "rdata_exchange")?)?),
            other => return Err(format!("record type {other} is outside the control subset").into()),
        };
        out.push(json!({"name": name(data, buf, layer, get(&fields, "name")?)?, "type": rtype,
                        "class": number(get(&fields, "class")?)?, "ttl": number(get(&fields, "ttl")?)?,
                        "rdata": rdata}));
    }
    Ok(out)
}

/// Decode one local DNS message with packet-dissector-dns's documented DnsDissector
/// (Dissector::dissect on caller-supplied bytes at offset 0) and walk its field tree.
pub fn parse(data: &[u8]) -> Res<Value> {
    if data.is_empty() || data.len() > 65535 {
        return Err("input outside harness limit".into());
    }
    let mut buf = DissectBuffer::new();
    DnsDissector.dissect(data, &mut buf, 0)?;
    let layer = buf.layers().first().ok_or("no DNS layer")?.clone();
    let header = |key: &str| -> Res<u64> { number(buf.field_by_name(&layer, key).ok_or(format!("missing {key}"))?) };
    let mut questions = Vec::new();
    if let Some(array) = buf.field_by_name(&layer, "questions") {
        for entry in entries(&buf, array)? {
            let fields = object(&buf, entry)?;
            questions.push(json!({"name": name(data, &buf, &layer, get(&fields, "name")?)?,
                                  "type": number(get(&fields, "type")?)?,
                                  "class": number(get(&fields, "class")?)?}));
        }
    }
    let mut out = Map::new();
    for key in ["id", "qr", "opcode", "aa", "tc", "rd", "ra"] {
        out.insert(key.into(), header(key)?.into());
    }
    out.insert("z".into(), ((header("z")? << 2) | (header("ad")? << 1) | header("cd")?).into());
    for key in ["rcode", "qdcount", "ancount", "nscount", "arcount"] {
        out.insert(key.into(), header(key)?.into());
    }
    out.insert("questions".into(), questions.into());
    out.insert("answers".into(), records(data, &buf, &layer, "answers")?.into());
    out.insert("authority".into(), records(data, &buf, &layer, "authorities")?.into());
    out.insert("additional".into(), records(data, &buf, &layer, "additionals")?.into());
    Ok(Value::Object(out))
}
