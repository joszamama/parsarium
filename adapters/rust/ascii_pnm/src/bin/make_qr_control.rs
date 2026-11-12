fn main() -> Result<(), Box<dyn std::error::Error>> {
    let code = roka_qr::Encoder::new(b"Parsarium P1 control").build()?;
    let pbm = code.render().scale(1).build().to_pbm();
    let path = std::env::args()
        .nth(1)
        .ok_or("usage: make_qr_control CONTROL.pbm")?;
    std::fs::write(path, pbm)?;
    Ok(())
}
