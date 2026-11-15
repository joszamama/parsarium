#[derive(Debug, PartialEq, Eq)]
pub struct Parsed {
    pub headers: usize,
    pub method: String,
    pub minor: u8,
    pub target: String,
}

pub fn parse(data: &[u8]) -> Result<Parsed, Box<dyn std::error::Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input size outside harness limit".into());
    }
    let mut headers = [httparse::EMPTY_HEADER; 16];
    let mut request = httparse::Request::new(&mut headers);
    if !request.parse(data)?.is_complete() { return Err("incomplete request".into()); }
    Ok(Parsed {
        headers: request.headers.len(),
        method: request.method.ok_or("missing method")?.to_owned(),
        minor: request.version.ok_or("missing version")?,
        target: request.path.ok_or("missing path")?.to_owned(),
    })
}
