use serde::Deserialize;
use serde_json::json;
use std::{env, fs, io::Cursor};

#[derive(Deserialize)]
struct Vertex { x: f32, y: f32, z: f32 }

#[derive(Deserialize)]
struct Face { vertex_indices: Vec<i32> }

#[derive(Deserialize)]
struct Mesh { vertex: Vec<Vertex>, face: Vec<Face> }

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 { return Err("usage: parsarium-rust-ascii-ply PACKAGE CONTROL.ply".into()); }
    let bytes = fs::read(&args[2])?;
    let output = match args[1].as_str() {
        "ply-rs-bw" => {
            let parser = ply_rs_bw::parser::Parser::<ply_rs_bw::ply::DefaultElement>::new();
            let ply = parser.read_ply(&mut Cursor::new(&bytes))?;
            json!({"vertices": ply.payload.get("vertex").map_or(0, Vec::len),
                   "faces": ply.payload.get("face").map_or(0, Vec::len),
                   "format": format!("{:?}", ply.header.encoding)})
        }
        "ply-rs" => {
            let parser = ply_rs::parser::Parser::<ply_rs::ply::DefaultElement>::new();
            let ply = parser.read_ply(&mut Cursor::new(&bytes))?;
            json!({"vertices": ply.payload.get("vertex").map_or(0, Vec::len),
                   "faces": ply.payload.get("face").map_or(0, Vec::len),
                   "format": format!("{:?}", ply.header.encoding)})
        }
        "serde-ply" => {
            let mesh: Mesh = serde_ply::from_bytes(&bytes)?;
            json!({"vertices": mesh.vertex.len(), "faces": mesh.face.len(),
                   "last_vertex": [mesh.vertex[2].x, mesh.vertex[2].y, mesh.vertex[2].z],
                   "first_face": mesh.face[0].vertex_indices})
        }
        "threecrate-io" => {
            let data = threecrate_io::ply::RobustPlyReader::read_ply_data(
                &mut std::io::BufReader::new(Cursor::new(&bytes)))?;
            json!({"vertices": data.elements.get("vertex").map_or(0, Vec::len),
                   "faces": data.elements.get("face").map_or(0, Vec::len),
                   "format": format!("{:?}", data.header.format)})
        }
        "brepkit-io" => {
            let mesh = brepkit_io::ply::read_ply(&bytes)?;
            json!({"vertices": mesh.positions.len(), "faces": mesh.indices.len() / 3})
        }
        "draco-io" => {
            let mut reader = draco_io::ply_reader::PlyReader::from_bytes(bytes.clone());
            let positions = reader.read_positions()?;
            json!({"vertices": positions.len(), "last_vertex": positions[2]})
        }
        "wblidar" => {
            use wblidar::io::PointReader;
            let mut reader = wblidar::ply::PlyReader::new(Cursor::new(&bytes))?;
            let points = reader.read_all()?;
            json!({"vertices": points.len(),
                   "last_vertex": [points[2].x, points[2].y, points[2].z]})
        }
        "rigidity-io" => {
            let cloud = rigidity_io::read_ply(std::path::Path::new(&args[2]))?;
            json!({"vertices": cloud.len()})
        }
        "cortenforge-mesh-io" => {
            let mesh = mesh_io::load_ply(&args[2])?;
            json!({"vertices": mesh.vertices.len(), "faces": mesh.faces.len()})
        }
        "point-formats" => {
            let geometry = point_formats::io::ply::read(
                &mut std::io::BufReader::new(Cursor::new(&bytes)))?;
            json!({"vertices": geometry.point_count(), "faces": geometry.face_count()})
        }
        "ferrum_cloud" => {
            let cloud = ferrum_cloud::io::load_ply(&args[2])?;
            json!({"vertices": cloud.len()})
        }
        "modelz" => {
            let model = modelz::Model3D::from_format(&args[2], &modelz::ModelFormat::PLY)
                .map_err(|error| format!("{error:?}"))?;
            json!({"meshes": model.meshes.len(),
                   "vertices": model.meshes.iter().map(|mesh| mesh.vertices.len()).sum::<usize>()})
        }
        "threecrate" => {
            let data = threecrate::io::ply::RobustPlyReader::read_ply_data(
                &mut std::io::BufReader::new(Cursor::new(&bytes)))?;
            json!({"vertices": data.elements.get("vertex").map_or(0, Vec::len),
                   "faces": data.elements.get("face").map_or(0, Vec::len)})
        }
        "terrio" => {
            let mut reader = terrio::pointcloud::open_points_bytes(bytes.clone(), "triangle.ply")?;
            let cloud = reader.read(&terrio::pointcloud::PointReadOptions::default())?;
            json!({"vertices": cloud.len()})
        }
        "rs-read-trimesh" => {
            let mesh = rs_read_trimesh::load_trimesh(&args[2], 1.0)?;
            json!({"vertices": mesh.vertices().len(), "faces": mesh.indices().len()})
        }
        "ply2splat" => {
            let points = ply2splat::load_ply_from_bytes(&bytes)?;
            json!({"vertices": points.len(),
                   "last_vertex": [points[2].x, points[2].y, points[2].z]})
        }
        "cumulus3d-core" => {
            let cloud = cumulus3d_core::io::read_ply(&args[2])?;
            json!({"vertices": cloud.len()})
        }
        "kosm-scan" => {
            let cloud = kosm_scan::paint::read_colour_cloud(std::path::Path::new(&args[2]))?;
            json!({"vertices": cloud.points.len(), "last_colour": cloud.colours[2]})
        }
        "voxel-tiler-core" => {
            type Cloud = voxel_tiler_core::collection::PointCloud<
                voxel_tiler_core::ordered_float::OrderedFloat<f32>, u8, u8>;
            let cloud = Cloud::from_ply(Cursor::new(&bytes));
            json!({"vertices": cloud.field.len()})
        }
        "zumen-ply" => {
            use zumen_sdk::Codec;
            let mut budget = zumen_base::budget::Budget::default();
            let mut diagnostics = zumen_base::diag::Diagnostics::default();
            let cancel = zumen_base::cancel::CancelToken::new();
            let mut context = zumen_sdk::Cx::new(&mut budget, &mut diagnostics, &cancel);
            let data = zumen_ply::Ply::read(&bytes, &mut context)
                .map_err(|error| format!("{error:?}"))?;
            json!({"format": format!("{:?}", data.encoding),
                   "vertices": data.elements.iter().find(|item| item.name == "vertex")
                       .map_or(0, |item| item.count),
                   "faces": data.elements.iter().find(|item| item.name == "face")
                       .map_or(0, |item| item.count)})
        }
        other => return Err(format!("unknown package: {other}").into()),
    };
    println!("{output}");
    Ok(())
}
