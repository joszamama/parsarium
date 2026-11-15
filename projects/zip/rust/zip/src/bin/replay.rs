use parsarium_zip_crate_harness::parse;
use std::env;
use std::fs;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = env::args().nth(1).ok_or("expected control path")?;
    let data = fs::read(path)?;
    let result = parse(&data)?;
    println!("{}", serde_json::json!({
        "name": result.name,
        "content": result.content,
        "size": result.size,
    }));
    Ok(())
}
