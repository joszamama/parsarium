use std::error::Error;
use std::io::Cursor;

/// Walk the MPEG audio frame headers of an untagged MP3 byte stream and sum their durations.
pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let duration = mp3_duration::from_read(&mut Cursor::new(data))?;
    let duration_ns = u64::try_from(duration.as_nanos())?;
    Ok(serde_json::json!({"duration_ns": duration_ns}))
}
