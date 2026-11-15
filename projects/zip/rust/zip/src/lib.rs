use std::io::{Cursor, Read};

#[derive(Debug, PartialEq, Eq)]
pub struct Parsed {
    pub name: String,
    pub content: String,
    pub size: u64,
}

pub fn parse(data: &[u8]) -> Result<Parsed, Box<dyn std::error::Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input size outside harness limit".into());
    }
    let mut archive = zip::ZipArchive::new(Cursor::new(data))?;
    let mut entry = archive.by_index(0)?;
    let name = entry.name()?.to_string();
    let size = entry.size();
    if size > (1 << 20) {
        return Err("decoded entry outside harness limit".into());
    }
    let mut content = String::new();
    entry.read_to_string(&mut content)?;
    Ok(Parsed { name, content, size })
}
