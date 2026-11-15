#[derive(Debug, PartialEq)]
pub struct Parsed {
    pub width: f32,
    pub height: f32,
    pub nodes: usize,
}

pub fn parse(data: &[u8]) -> Result<Parsed, Box<dyn std::error::Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input size outside harness limit".into());
    }
    let tree = usvg::Tree::from_data(data, &usvg::Options::default())?;
    Ok(Parsed { width: tree.size().width(), height: tree.size().height(),
                nodes: tree.root().children().len() })
}
