use parsarium_http11_weida_http_codec_harness::parse;
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = std::env::args().nth(1).ok_or("expected input path")?;
    println!("{}", parse(&std::fs::read(path)?)?);
    Ok(())
}
