use std::error::Error;
use std::fs::File;
use std::path::Path;

fn parse_package(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let result = match package {
        "vsd-mp4" => {
            use std::cell::Cell;
            use std::rc::Rc;
            let timescale = Rc::new(Cell::new(None));
            let callback_timescale = Rc::clone(&timescale);
            let mut parser = vsd_mp4::Mp4Parser::new()
                .base_box("moov", vsd_mp4::children)
                .full_box("mvhd", move |mut movie| {
                    if movie.version == Some(0) {
                        movie.reader.skip(8)?;
                        callback_timescale.set(Some(movie.reader.read_u32()?));
                    }
                    Ok(())
                });
            parser.parse(&std::fs::read(path)?, false, false)?;
            serde_json::json!({"movie_timescale":timescale.get().ok_or("no mvhd timescale")?})
        }
        _ => return Err(format!("unknown package: {package}").into()),
    };
    Ok(result)
}


use std::sync::atomic::{AtomicU64, Ordering};
static NEXT_INPUT: AtomicU64 = AtomicU64::new(0);

pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let path = std::env::temp_dir().join(format!(
        "parsarium-rust-{}-{}.mp4",
        std::process::id(), NEXT_INPUT.fetch_add(1, Ordering::Relaxed)));
    std::fs::write(&path, data)?;
    let outcome = parse_package("vsd-mp4", &path);
    std::fs::remove_file(path)?;
    outcome
}
