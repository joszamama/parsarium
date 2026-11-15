use parsarium_png_crate_harness::parse;
use std::env;
use std::fs;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = env::args().nth(1).ok_or("expected control path")?;
    let data = fs::read(path)?;
    let result = parse(&data)?;
    println!(
        "{{\"width\":{},\"height\":{},\"red_0_0\":{}}}",
        result.width, result.height, result.red_0_0
    );
    Ok(())
}
