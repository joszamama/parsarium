use std::error::Error;

use serde_json::{Map, Value as Json, json};
use toml::value::{Datetime, Offset};
use toml::{Table, Value};

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

fn fraction(nanosecond: Option<u32>) -> String {
    match nanosecond {
        Some(nanos) if nanos > 0 => {
            let digits = format!("{nanos:09}");
            format!(".{}", digits.trim_end_matches('0'))
        }
        _ => String::new(),
    }
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

/// Format toml's Datetime parts; an offset date-time becomes its UTC instant.
fn datetime(value: &Datetime) -> Result<Json, Box<dyn Error>> {
    match (value.date, value.time, value.offset) {
        (Some(date), Some(time), Some(offset)) => {
            let minutes = match offset {
                Offset::Z => 0,
                Offset::Custom { minutes } => i64::from(minutes),
            };
            let second = i64::from(time.second.unwrap_or(0));
            let local = days_from_civil(i64::from(date.year), i64::from(date.month), i64::from(date.day))
                * 86_400
                + i64::from(time.hour) * 3600
                + i64::from(time.minute) * 60
                + second;
            let utc = local - minutes * 60;
            let (year, month, day) = civil_from_days(utc.div_euclid(86_400));
            let rest = utc.rem_euclid(86_400);
            Ok(scalar("datetime", format!(
                "{year:04}-{month:02}-{day:02}T{:02}:{:02}:{:02}{}Z",
                rest / 3600, rest % 3600 / 60, rest % 60, fraction(time.nanosecond))))
        }
        (Some(date), Some(time), None) => Ok(scalar("datetime-local", format!(
            "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}{}",
            date.year, date.month, date.day, time.hour, time.minute,
            time.second.unwrap_or(0), fraction(time.nanosecond)))),
        (Some(date), None, None) => Ok(scalar("date-local", format!(
            "{:04}-{:02}-{:02}", date.year, date.month, date.day))),
        (None, Some(time), None) => Ok(scalar("time-local", format!(
            "{:02}:{:02}:{:02}{}", time.hour, time.minute,
            time.second.unwrap_or(0), fraction(time.nanosecond)))),
        _ => Err(format!("unrepresentable datetime: {value:?}").into()),
    }
}

fn value(value: &Value) -> Result<Json, Box<dyn Error>> {
    Ok(match value {
        Value::String(text) => scalar("string", text.clone()),
        Value::Integer(number) => scalar("integer", number.to_string()),
        Value::Float(number) => scalar("float", float_text(*number)),
        Value::Boolean(flag) => scalar("bool", flag.to_string()),
        Value::Datetime(moment) => datetime(moment)?,
        Value::Array(items) => Json::Array(items.iter().map(self::value).collect::<Result<_, _>>()?),
        Value::Table(entries) => table(entries)?,
    })
}

fn table(entries: &Table) -> Result<Json, Box<dyn Error>> {
    let mut object = Map::new();
    for (key, item) in entries {
        object.insert(key.clone(), value(item)?);
    }
    Ok(Json::Object(object))
}

/// Parse one local TOML buffer with toml's documented `from_str::<toml::Table>(&str)`
/// API. toml lexes and parses through the toml_parser crate and builds its own
/// Table/Value tree; the harness only walks that tree. The bytes are decoded as
/// UTF-8 locally first. serde_json only encodes the observed typed tree.
pub fn parse(data: &[u8]) -> Result<Json, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let document: Table = toml::from_str(text)?;
    table(&document)
}
