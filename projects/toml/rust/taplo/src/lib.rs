use std::error::Error;
use std::sync::Once;
use std::sync::atomic::{AtomicUsize, Ordering};

use serde_json::{Map, Value as Json, json};
use taplo::dom::Node;
use taplo::dom::node::{DateTimeValue, IntegerValue};

fn scalar(kind: &str, value: String) -> Json {
    json!({"type": kind, "value": value})
}

/// Shortest round-trip digits from Rust's `f64` Display (always positional),
/// with at least one fractional digit.
fn float_text(value: f64) -> String {
    if value.is_nan() {
        return "nan".to_string();
    }
    if value.is_infinite() {
        return if value > 0.0 { "inf" } else { "-inf" }.to_string();
    }
    let text = format!("{value}");
    if text.contains('.') { text } else { format!("{text}.0") }
}

fn fraction(nanosecond: u32) -> String {
    if nanosecond == 0 {
        return String::new();
    }
    let digits = format!("{nanosecond:09}");
    format!(".{}", digits.trim_end_matches('0'))
}

fn date_text(date: time::Date) -> String {
    format!("{:04}-{:02}-{:02}", date.year(), u8::from(date.month()), date.day())
}

fn time_text(clock: time::Time) -> String {
    format!("{:02}:{:02}:{:02}{}", clock.hour(), clock.minute(), clock.second(), fraction(clock.nanosecond()))
}

/// taplo's DateTimeValue holds `time` crate values; an offset date-time becomes its UTC instant
/// through `OffsetDateTime::to_offset(UTC)`.
fn datetime(value: DateTimeValue) -> Json {
    match value {
        DateTimeValue::OffsetDateTime(moment) => {
            let utc = moment.to_offset(time::UtcOffset::UTC);
            scalar("datetime", format!("{}T{}Z", date_text(utc.date()), time_text(utc.time())))
        }
        DateTimeValue::LocalDateTime(moment) => {
            scalar("datetime-local", format!("{}T{}", date_text(moment.date()), time_text(moment.time())))
        }
        DateTimeValue::Date(date) => scalar("date-local", date_text(date)),
        DateTimeValue::Time(clock) => scalar("time-local", time_text(clock)),
    }
}

fn node(value: &Node) -> Result<Json, Box<dyn Error>> {
    Ok(match value {
        Node::Table(table) => {
            let mut object = Map::new();
            for (key, child) in table.entries().read().iter() {
                if object.insert(key.value().to_string(), node(child)?).is_some() {
                    return Err(format!("duplicate key {}", key.value()).into());
                }
            }
            Json::Object(object)
        }
        Node::Array(array) => Json::Array(array.items().read().iter().map(node).collect::<Result<_, _>>()?),
        Node::Bool(flag) => scalar("bool", flag.value().to_string()),
        Node::Str(text) => scalar("string", text.value().to_string()),
        Node::Integer(number) => scalar("integer", match number.value() {
            IntegerValue::Negative(value) => value.to_string(),
            IntegerValue::Positive(value) => value.to_string(),
        }),
        Node::Float(number) => scalar("float", float_text(number.value())),
        Node::Date(moment) => datetime(moment.value()),
        Node::Invalid(_) => return Err("invalid node".into()),
    })
}

/// taplo's DOM keeps an `ahash::AHashMap` lookup index per table. ahash's default per-map
/// seed source adds the addresses of a static and of its own allocation, which ASLR moves
/// between processes, so the hashbrown probe code monomorphized into taplo took different
/// branches from run to run. A fixed seed source (ahash's documented
/// `random_state::set_random_source`) makes each process hash the same way; taplo's
/// parser and the DOM it returns are unchanged.
struct FixedSeeds(AtomicUsize);

impl ahash::random_state::RandomSource for FixedSeeds {
    fn gen_hasher_seed(&self) -> usize {
        self.0.fetch_add(0x9e37_79b9, Ordering::Relaxed)
    }
}

fn fix_hash_seeds() {
    static ONCE: Once = Once::new();
    ONCE.call_once(|| {
        let _ = ahash::random_state::set_random_source(FixedSeeds(AtomicUsize::new(0x5a5a_5a5a)));
    });
}

/// Parse one local TOML buffer with taplo's documented `taplo::parser::parse(&str)`, which
/// lexes (logos) and parses the text into a rowan syntax tree, then `Parse::into_dom()`, which
/// builds taplo's DOM (tables with merged dotted and header keys, arrays and typed values).
/// Syntax errors and DOM semantic errors (`Node::validate`) are rejected. The harness only
/// walks the DOM; the bytes are decoded as UTF-8 locally first, and serde_json only encodes
/// the observed typed tree.
pub fn parse(data: &[u8]) -> Result<Json, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    fix_hash_seeds();
    let parsed = taplo::parser::parse(text);
    if !parsed.errors.is_empty() {
        return Err(format!("syntax errors: {:?}", parsed.errors).into());
    }
    let dom = parsed.into_dom();
    if let Err(errors) = dom.validate() {
        return Err(format!("semantic errors: {:?}", errors.collect::<Vec<_>>()).into());
    }
    node(&dom)
}
