use parsarium_mp4_lofty_harness::parse;
fn run() -> Result<(), Box<dyn std::error::Error>> {
    let path = std::env::args().nth(1).ok_or("expected input path")?;
    println!("{}", parse(&std::fs::read(path)?)?);
    Ok(())
}
fn main() {
    // Print the error's message (Display); its Debug form leaves the message out.
    if let Err(error) = run() {
        eprintln!("Error: {error}");
        std::process::exit(1);
    }
}
