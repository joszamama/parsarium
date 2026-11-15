use parsarium_ascii_pnm_image_harness::parse;
use std::env;
use std::fs;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = env::args().nth(1).ok_or("expected control path")?;
    let data = fs::read(path)?;
    let result = parse(&data)?;
    println!("{}", serde_json::json!({
        "width": result.width,
        "height": result.height,
        "rgb": result.rgb,
    }));
    Ok(())
}
