use serde_json::json;
use std::{env, fs};

#[derive(Default)]
struct UrlCapture {
    url: Vec<u8>,
    message_complete: bool,
}

impl http_muncher::ParserHandler for UrlCapture {
    fn on_url(&mut self, _: &mut http_muncher::Parser, data: &[u8]) -> bool {
        self.url.extend_from_slice(data);
        true
    }
    fn on_message_complete(&mut self, _: &mut http_muncher::Parser) -> bool {
        self.message_complete = true;
        true
    }
}

impl http_parser::HttpParserCallback for UrlCapture {
    fn on_url(&mut self, _: &mut http_parser::HttpParser, data: &[u8]) -> http_parser::CallbackResult {
        self.url.extend_from_slice(data);
        Ok(http_parser::ParseAction::None)
    }
    fn on_message_complete(&mut self, _: &mut http_parser::HttpParser) -> http_parser::CallbackResult {
        self.message_complete = true;
        Ok(http_parser::ParseAction::None)
    }
}

fn utf8(bytes: &[u8]) -> Result<&str, Box<dyn std::error::Error>> {
    Ok(std::str::from_utf8(bytes)?)
}

fn parse_package(package: &str, path: &std::path::Path) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    let args: Vec<String> = vec!["parser".into(), package.into(), path.to_string_lossy().into_owned()];
    if args.len() != 3 {
        return Err("usage: parsarium-rust-http11 PACKAGE CONTROL.http".into());
    }
    let bytes = fs::read(&args[2])?;
    let output = match args[1].as_str() {
        "async-h1" => {
            let mut response = futures_lite::future::block_on(
                async_h1::client::decode(futures_lite::io::Cursor::new(bytes.clone())))?;
            let status = response.status() as u16;
            let body = futures_lite::future::block_on(response.body_string())?;
            json!({"status": status, "body": body})
        }
        other => return Err(format!("unknown package: {other}").into()),
    };
    Ok(output)
}

use std::sync::atomic::{AtomicU64, Ordering};
static NEXT_INPUT: AtomicU64 = AtomicU64::new(0);

pub fn parse(data: &[u8]) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    if data.is_empty() || data.len() > (1 << 20) {
        return Err("input outside harness limit".into());
    }
    let path = std::env::temp_dir().join(format!(
        "parsarium-rust-{}-{}.http",
        std::process::id(), NEXT_INPUT.fetch_add(1, Ordering::Relaxed)));
    std::fs::write(&path, data)?;
    let outcome = parse_package("async-h1", &path);
    std::fs::remove_file(path)?;
    outcome
}
