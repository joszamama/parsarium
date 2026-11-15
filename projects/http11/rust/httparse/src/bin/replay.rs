use parsarium_http11_httparse_harness::parse;
use std::env;
use std::fs;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = env::args().nth(1).ok_or("expected control path")?;
    let result = parse(&fs::read(path)?)?;
    println!("{}", serde_json::json!({
        "headers": result.headers,
        "method": result.method,
        "minor": result.minor,
        "target": result.target,
    }));
    Ok(())
}
