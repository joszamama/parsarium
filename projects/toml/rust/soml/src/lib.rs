use std::error::Error;

use serde_json::{Value as Json, json};

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

/// Days since 1970-01-01 for a proleptic Gregorian date (Howard Hinnant's algorithm).
fn days_from_civil(year: i64, month: i64, day: i64) -> i64 {
    let year = if month <= 2 { year - 1 } else { year };
    let era = year.div_euclid(400);
    let yoe = year - era * 400;
    let mp = (month + 9) % 12;
    let doy = (153 * mp + 2) / 5 + day - 1;
    let doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    era * 146_097 + doe - 719_468
}

fn civil_from_days(days: i64) -> (i64, i64, i64) {
    let z = days + 719_468;
    let era = z.div_euclid(146_097);
    let doe = z - era * 146_097;
    let yoe = (doe - doe / 1460 + doe / 36_524 - doe / 146_096) / 365;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let day = doy - (153 * mp + 2) / 5 + 1;
    let month = if mp < 10 { mp + 3 } else { mp - 9 };
    (if month <= 2 { yoe + era * 400 + 1 } else { yoe + era * 400 }, month, day)
}

/// Format date-time parts read from the library's own type; an offset date-time
/// (offset in minutes east of UTC) becomes its UTC instant.
fn datetime(date: Option<(i64, i64, i64)>, time: Option<(i64, i64, i64, u32)>, offset: Option<i64>)
    -> Result<Json, Box<dyn Error>> {
    match (date, time, offset) {
        (Some((y, mo, d)), Some((h, mi, s, ns)), Some(minutes)) => {
            let utc = days_from_civil(y, mo, d) * 86_400 + h * 3600 + mi * 60 + s - minutes * 60;
            let (year, month, day) = civil_from_days(utc.div_euclid(86_400));
            let rest = utc.rem_euclid(86_400);
            Ok(scalar("datetime", format!(
                "{year:04}-{month:02}-{day:02}T{:02}:{:02}:{:02}{}Z",
                rest / 3600, rest % 3600 / 60, rest % 60, fraction(ns))))
        }
        (Some((y, mo, d)), Some((h, mi, s, ns)), None) => Ok(scalar("datetime-local", format!(
            "{y:04}-{mo:02}-{d:02}T{h:02}:{mi:02}:{s:02}{}", fraction(ns)))),
        (Some((y, mo, d)), None, None) => Ok(scalar("date-local", format!("{y:04}-{mo:02}-{d:02}"))),
        (None, Some((h, mi, s, ns)), None) => Ok(scalar("time-local", format!(
            "{h:02}:{mi:02}:{s:02}{}", fraction(ns)))),
        _ => Err("unrepresentable date-time".into()),
    }
}

use serde_json::Map;
use soml::{Table, Value, value::Offset};

fn value(node: &Value) -> Result<Json, Box<dyn Error>> {
    Ok(match node {
        Value::String(text) => scalar("string", text.clone()),
        Value::Integer(number) => scalar("integer", number.to_string()),
        Value::Float(number) => scalar("float", float_text(*number)),
        Value::Boolean(flag) => scalar("bool", flag.to_string()),
        Value::Datetime(moment) => datetime(
            moment.date.as_ref().map(|d| (i64::from(d.year), i64::from(d.month), i64::from(d.day))),
            moment.time.as_ref().map(|t| (i64::from(t.hour), i64::from(t.minute), i64::from(t.second), t.nanosecond)),
            moment.offset.as_ref().map(|o| match o {
                &Offset::Z => 0,
                &Offset::Custom { minutes } => i64::from(minutes),
            }),
        )?,
        Value::Array(items) => Json::Array(items.iter().map(value).collect::<Result<_, _>>()?),
        Value::Table(entries) => table(entries)?,
    })
}

fn table(entries: &Table) -> Result<Json, Box<dyn Error>> {
    let mut object = Map::new();
    for (key, child) in entries.iter() {
        if object.insert(key.to_string(), value(child)?).is_some() {
            return Err(format!("duplicate key {key}").into());
        }
    }
    Ok(Json::Object(object))
}

/// Parse one local TOML buffer with tomlproc's documented `tomlproc::parse(&str) -> Table`:
/// the crate's own dependency-free parser builds a plain value tree with typed integers,
/// floats and a Datetime type holding optional date, time and offset parts. The harness only
/// walks that tree; offset date-times are converted to the UTC instant arithmetically.
pub fn parse(data: &[u8]) -> Result<Json, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    table(&soml::from_str::<Table>(text).map_err(|error| error.to_string())?)
}
