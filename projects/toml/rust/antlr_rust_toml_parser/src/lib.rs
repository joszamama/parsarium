use std::error::Error;

use antlr_rust_toml_parser::{Assignment, Item, Value};
use serde_json::{Map, Value as Json, json};

fn scalar(kind: &str, value: String) -> Json {
    json!({"type": kind, "value": value})
}

/// The crate's documented `Value::Float` payload is its float token with the underscores
/// removed ("directly parseable", per its own test); `str::parse::<f64>` reads that payload and
/// Rust's `f64` Display writes the shortest round-trip digits positionally.
fn float_text(payload: &str) -> Result<String, Box<dyn Error>> {
    match payload {
        "inf" | "+inf" => return Ok("inf".to_string()),
        "-inf" => return Ok("-inf".to_string()),
        "nan" | "+nan" | "-nan" => return Ok("nan".to_string()),
        _ => {}
    }
    let value: f64 = payload.parse()?;
    let text = format!("{value}");
    Ok(if text.contains('.') { text } else { format!("{text}.0") })
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

/// Format the `toml_datetime::Datetime` the crate returns; an offset date-time becomes its
/// UTC instant.
fn datetime(value: &toml_datetime::Datetime) -> Result<Json, Box<dyn Error>> {
    use toml_datetime::Offset;
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
                rest / 3600, rest % 3600 / 60, rest % 60, fraction(time.nanosecond.unwrap_or(0)))))
        }
        (Some(date), Some(time), None) => Ok(scalar("datetime-local", format!(
            "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}{}",
            date.year, date.month, date.day, time.hour, time.minute, time.second.unwrap_or(0),
            fraction(time.nanosecond.unwrap_or(0))))),
        (Some(date), None, None) => Ok(scalar("date-local", format!(
            "{:04}-{:02}-{:02}", date.year, date.month, date.day))),
        (None, Some(time), None) => Ok(scalar("time-local", format!(
            "{:02}:{:02}:{:02}{}", time.hour, time.minute, time.second.unwrap_or(0),
            fraction(time.nanosecond.unwrap_or(0))))),
        _ => Err(format!("unrepresentable datetime: {value:?}").into()),
    }
}

fn value(node: &Value) -> Result<Json, Box<dyn Error>> {
    Ok(match node {
        Value::String(text) => scalar("string", text.clone()),
        Value::Integer(number) => scalar("integer", number.to_string()),
        Value::Float(payload) => scalar("float", float_text(payload)?),
        Value::Boolean(flag) => scalar("bool", flag.to_string()),
        Value::DateTime(moment) => datetime(moment)?,
        Value::Array(items) => Json::Array(items.iter().map(value).collect::<Result<_, _>>()?),
        Value::InlineTable(entries) => {
            let mut table = Map::new();
            for entry in entries {
                assign(&mut table, entry)?;
            }
            Json::Object(table)
        }
    })
}

/// Follow `segments` from `table`, creating implicit tables; an array of tables is entered
/// through its last element (the table the most recent `[[...]]` header opened).
fn descend<'a>(mut table: &'a mut Map<String, Json>, segments: &[String])
    -> Result<&'a mut Map<String, Json>, Box<dyn Error>> {
    for segment in segments {
        let slot = table.entry(segment.clone()).or_insert_with(|| Json::Object(Map::new()));
        let slot = match slot {
            Json::Array(items) => items.last_mut().ok_or("empty array of tables")?,
            other => other,
        };
        table = match slot {
            Json::Object(inner) if !inner.contains_key("type") || !inner.contains_key("value") => inner,
            _ => return Err(format!("key {segment} is not a table").into()),
        };
    }
    Ok(table)
}

fn assign(table: &mut Map<String, Json>, entry: &Assignment) -> Result<(), Box<dyn Error>> {
    let segments = entry.key().segments();
    let (last, parents) = segments.split_last().ok_or("empty key")?;
    let target = descend(table, parents)?;
    if target.insert(last.clone(), value(entry.value())?).is_some() {
        return Err(format!("duplicate key {last}").into());
    }
    Ok(())
}

/// Parse one local TOML buffer with antlr-rust-toml-parser's documented
/// `antlr_rust_toml_parser::parse(&str) -> Document`: the crate's checked-in ANTLR-generated
/// lexer and parser recognize the text and its decoder returns flat items in source order
/// (key/value assignments with typed `Value`s and `[table]`/`[[array]]` headers). As the
/// README states, table nesting is left to the consumer, so the harness places each
/// assignment under the most recent header; it never re-reads the input text.
pub fn parse(data: &[u8]) -> Result<Json, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let document = antlr_rust_toml_parser::parse(text).map_err(|error| error.to_string())?;
    let mut root = Map::new();
    let mut current: Vec<String> = Vec::new();
    for item in document.items() {
        match item {
            Item::Assignment(entry) => assign(descend(&mut root, &current)?, entry)?,
            Item::Table(header) => {
                let segments = header.key().segments();
                if header.is_array() {
                    let (last, parents) = segments.split_last().ok_or("empty header")?;
                    let parent = descend(&mut root, parents)?;
                    let slot = parent.entry(last.clone()).or_insert_with(|| Json::Array(Vec::new()));
                    let Json::Array(items) = slot else {
                        return Err(format!("key {last} is not an array of tables").into());
                    };
                    items.push(Json::Object(Map::new()));
                } else {
                    descend(&mut root, segments)?;
                }
                current = segments.to_vec();
            }
        }
    }
    Ok(Json::Object(root))
}
