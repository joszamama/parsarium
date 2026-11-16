use serde::Deserialize;
use serde_json::json;
use std::{env, fs, io::Cursor};

#[derive(Deserialize)]
struct Vertex { x: f32, y: f32, z: f32 }

#[derive(Deserialize)]
struct Face { vertex_indices: Vec<i32> }

#[derive(Deserialize)]
struct Mesh { vertex: Vec<Vertex>, face: Vec<Face> }

fn parse_package(package: &str, path: &std::path::Path) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    let args: Vec<String> = vec!["parser".into(), package.into(), path.to_string_lossy().into_owned()];
    if args.len() != 3 { return Err("usage: parsarium-rust-ascii-ply PACKAGE CONTROL.ply".into()); }
    let bytes = fs::read(&args[2])?;
    let output = match args[1].as_str() {
        "ply2splat" => {
            let points = ply2splat::load_ply_from_bytes(&bytes)?;
            json!({"vertices": points.len(),
                   "last_vertex": [points[2].x, points[2].y, points[2].z]})
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
        "parsarium-rust-{}-{}.ply",
        std::process::id(), NEXT_INPUT.fetch_add(1, Ordering::Relaxed)));
    std::fs::write(&path, data)?;
    let outcome = parse_package("ply2splat", &path);
    std::fs::remove_file(path)?;
    outcome
}
