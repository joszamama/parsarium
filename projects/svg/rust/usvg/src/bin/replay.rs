use parsarium_svg_usvg_harness::parse;
use std::env;
use std::fs;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = env::args().nth(1).ok_or("expected control path")?;
    let result = parse(&fs::read(path)?)?;
    println!("{}", serde_json::json!({
        "width": result.width,
        "height": result.height,
        "nodes": result.nodes,
    }));
    Ok(())
}
