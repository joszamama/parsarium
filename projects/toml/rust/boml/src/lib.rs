use std::error::Error;

use boml::table::TomlTable;
use boml::types::{OffsetTomlDateTime, TomlDate, TomlTime, TomlValue};
use serde_json::{Map, Value as Json, json};

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

fn date_text(date: &TomlDate) -> String {
    format!("{:04}-{:02}-{:02}", date.year, date.month, date.month_day)
}

fn time_text(clock: &TomlTime) -> String {
    format!("{:02}:{:02}:{:02}{}", clock.hour, clock.minute, clock.second, fraction(clock.nanosecond))
}

/// boml keeps the written offset (signed hours, unsigned minutes); the offset date-time
/// becomes its UTC instant arithmetically.
fn utc_instant(value: &OffsetTomlDateTime) -> String {
    let hours = i64::from(value.offset.hour);
    let minutes = i64::from(value.offset.minute);
    let offset = hours * 60 + if hours < 0 { -minutes } else { minutes };
    let local = days_from_civil(i64::from(value.date.year), i64::from(value.date.month),
                                i64::from(value.date.month_day)) * 86_400
        + i64::from(value.time.hour) * 3600
        + i64::from(value.time.minute) * 60
        + i64::from(value.time.second);
    let utc = local - offset * 60;
    let (year, month, day) = civil_from_days(utc.div_euclid(86_400));
    let rest = utc.rem_euclid(86_400);
    format!("{year:04}-{month:02}-{day:02}T{:02}:{:02}:{:02}{}Z",
            rest / 3600, rest % 3600 / 60, rest % 60, fraction(value.time.nanosecond))
}

fn value(item: &TomlValue) -> Result<Json, Box<dyn Error>> {
    Ok(match item {
        TomlValue::String(text) => scalar("string", text.as_str().to_string()),
        TomlValue::Integer(number) => scalar("integer", number.to_string()),
        TomlValue::Float(number) => scalar("float", float_text(*number)),
        TomlValue::Boolean(flag) => scalar("bool", flag.to_string()),
        TomlValue::OffsetDateTime(moment) => scalar("datetime", utc_instant(moment)),
        TomlValue::DateTime(moment) => {
            scalar("datetime-local", format!("{}T{}", date_text(&moment.date), time_text(&moment.time)))
        }
        TomlValue::Date(date) => scalar("date-local", date_text(date)),
        TomlValue::Time(clock) => scalar("time-local", time_text(clock)),
        TomlValue::Array(items) => Json::Array(items.iter().map(value).collect::<Result<_, _>>()?),
        TomlValue::Table(entries) => table(entries)?,
    })
}

fn table(entries: &TomlTable) -> Result<Json, Box<dyn Error>> {
    let mut object = Map::new();
    for (key, item) in entries.iter() {
        object.insert(key.as_str().to_string(), value(item)?);
    }
    Ok(Json::Object(object))
}

/// Parse one local TOML buffer with boml's documented `boml::parse(&str)`. The
/// dependency-free crate scans and parses the text itself and returns a TomlTable of typed
/// TomlValue variants; the harness only walks that tree. The bytes are decoded as UTF-8
/// locally first. serde_json only encodes the observed typed tree.
pub fn parse(data: &[u8]) -> Result<Json, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let text = std::str::from_utf8(data)?;
    let document = boml::parse(text).map_err(|error| format!("{:?}", error.kind))?;
    table(&document)
}
