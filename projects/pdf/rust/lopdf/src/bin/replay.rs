use parsarium_pdf_lopdf_harness::parse;
use std::{env, fs};
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = env::args().nth(1).ok_or("expected control path")?;
    let parsed = parse(&fs::read(path)?)?;
    println!("{}", serde_json::json!({"pages": parsed.pages}));
    Ok(())
}
