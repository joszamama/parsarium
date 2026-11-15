#[derive(Debug, PartialEq, Eq)]
pub struct Parsed { pub pages: usize }
pub fn parse(data: &[u8]) -> Result<Parsed, Box<dyn std::error::Error>> {
    if data.is_empty() || data.len() > (1 << 20) { return Err("input outside harness limit".into()); }
    let document = lopdf::Document::load_mem(data)?;
    Ok(Parsed { pages: document.get_pages().len() })
}
