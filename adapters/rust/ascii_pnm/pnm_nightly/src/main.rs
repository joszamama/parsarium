use std::{env, fs};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = env::args()
        .nth(1)
        .ok_or("usage: parsarium-rust-pnm-nightly CONTROL.pnm")?;
    let bytes = fs::read(path)?;
    let image = pnm::decode(&bytes).map_err(|error| format!("{error:?}"))?;
    println!("{}", serde_json::json!({"parsed": format!("{image:?}")}));
    Ok(())
}
