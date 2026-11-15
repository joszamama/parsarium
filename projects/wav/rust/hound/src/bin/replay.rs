use parsarium_wav_hound_harness::parse;
use std::env;
use std::fs;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = env::args().nth(1).ok_or("expected control path")?;
    let data = fs::read(path)?;
    let result = parse(&data)?;
    println!("{}", serde_json::json!({
        "sample_rate": result.sample_rate,
        "channels": result.channels,
        "samples": result.samples,
    }));
    Ok(())
}
