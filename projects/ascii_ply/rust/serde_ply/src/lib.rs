use serde::Deserialize;
use serde::de::IgnoredAny;
use serde_json::json;
use std::collections::HashMap;
use std::{env, fs, io::Cursor};

#[derive(Deserialize)]
struct Vertex { x: f32, y: f32, z: f32 }

// PLY files name the face list vertex_indices or vertex_index.
#[derive(Deserialize)]
struct Face { #[serde(alias = "vertex_index")] vertex_indices: Vec<i32> }

// A point cloud has no face element. serde-ply cannot skip an element that the
// target type does not name, so the standard edge element is read as rows of
// properties and not reported.
#[derive(Deserialize)]
#[allow(dead_code)]
struct Mesh {
    vertex: Vec<Vertex>,
    #[serde(default)]
    face: Vec<Face>,
    #[serde(default)]
    edge: Vec<HashMap<String, IgnoredAny>>,
}

fn parse_package(package: &str, path: &std::path::Path) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    let args: Vec<String> = vec!["parser".into(), package.into(), path.to_string_lossy().into_owned()];
    if args.len() != 3 { return Err("usage: parsarium-rust-ascii-ply PACKAGE CONTROL.ply".into()); }
    let bytes = fs::read(&args[2])?;
    let output = match args[1].as_str() {
        "serde-ply" => {
            let mesh: Mesh = serde_ply::from_bytes(&bytes)?;
            let last_vertex = mesh.vertex.last().map(|v| vec![v.x, v.y, v.z]).unwrap_or_default();
            let first_face = mesh.face.first().map(|f| f.vertex_indices.clone()).unwrap_or_default();
            json!({"vertices": mesh.vertex.len(), "faces": mesh.face.len(),
                   "last_vertex": last_vertex, "first_face": first_face})
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
    let outcome = parse_package("serde-ply", &path);
    std::fs::remove_file(path)?;
    outcome
}
