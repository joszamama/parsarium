use std::error::Error;
use std::fs;
use std::io::{Cursor, Read};

fn output(name: &str, content: Option<&str>, size: u64) -> serde_json::Value {
    serde_json::json!({"name": name, "content": content, "size": size})
}

fn output_entry(name: &str, count: usize) -> serde_json::Value {
    serde_json::json!({"name": name, "entry_count": count})
}

fn parse_package(package: &str, path: &std::path::Path) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    let args: Vec<String> = std::vec!["parser".into(), package.into(), path.to_string_lossy().into_owned()];
    if args.len() != 3 {
        return Err("usage: parsarium-rust-zip PACKAGE CONTROL".into());
    }
    let bytes = fs::read(&args[2])?;
    match args[1].as_str() {
        "zip-extract" => {
            let root = tempfile::tempdir()?;
            let destination = root.path().join("out");
            install_logger();
            extracted().clear();
            #[allow(deprecated)]
            let result = zip_extract::extract(Cursor::new(&bytes), &destination, false);
            let visited = std::mem::take(&mut *extracted());
            result?;
            // zip-extract writes every entry and traces each one, in archive
            // order, as "Extracting NAME to PATH"; report the first entry.
            let first = visited.first().ok_or("zip-extract extracted no entry")?;
            let marker = format!(" to {}", destination.display());
            let split = first.find(&marker).ok_or("unexpected zip-extract trace")?;
            let name = first["Extracting ".len()..split].to_string();
            let target = std::path::PathBuf::from(&first[split + " to ".len()..]);
            if target.is_dir() {
                return Ok(output(&name, Some(""), 0));
            }
            let content = fs::read(&target)?;
            let size = content.len() as u64;
            let text = String::from_utf8(content).ok();
            return Ok(output(&name, text.as_deref(), size));
        }
        other => return Err(format!("unknown ZIP package: {other}").into()),
    }
    Err("parser produced no result".into())
}

struct ExtractLog;

impl log::Log for ExtractLog {
    fn enabled(&self, metadata: &log::Metadata) -> bool {
        metadata.target() == "zip_extract"
    }
    fn log(&self, record: &log::Record) {
        if record.target() == "zip_extract" && record.level() == log::Level::Trace {
            let message = record.args().to_string();
            if message.starts_with("Extracting ") {
                extracted().push(message);
            }
        }
    }
    fn flush(&self) {}
}

static EXTRACT_LOG: ExtractLog = ExtractLog;
static EXTRACTED: std::sync::Mutex<Vec<String>> = std::sync::Mutex::new(Vec::new());

fn extracted() -> std::sync::MutexGuard<'static, Vec<String>> {
    EXTRACTED.lock().unwrap_or_else(|poisoned| poisoned.into_inner())
}

fn install_logger() {
    if log::set_logger(&EXTRACT_LOG).is_ok() {
        log::set_max_level(log::LevelFilter::Trace);
    }
}

use std::sync::atomic::{AtomicU64, Ordering};
static NEXT_INPUT: AtomicU64 = AtomicU64::new(0);

pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let path = std::env::temp_dir().join(format!(
        "parsarium-rust-{}-{}.zip",
        std::process::id(), NEXT_INPUT.fetch_add(1, Ordering::Relaxed)));
    std::fs::write(&path, data)?;
    let outcome = parse_package("zip-extract", &path);
    std::fs::remove_file(path)?;
    outcome
}
