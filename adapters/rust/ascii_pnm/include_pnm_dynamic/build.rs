use std::{env, fs, path::Path};

fn main() {
    let path = env::var("PARSARIUM_PNM_CONTROL").expect("PARSARIUM_PNM_CONTROL is required");
    let path = Path::new(&path).canonicalize().expect("control must exist");
    let path = path.to_str().expect("control path must be UTF-8");
    assert!(
        !path.contains(['"', '\\']),
        "macro requires a simple quoted path"
    );
    println!("cargo:rerun-if-env-changed=PARSARIUM_PNM_CONTROL");
    println!("cargo:rerun-if-changed={path}");
    let out = Path::new(&env::var("OUT_DIR").unwrap()).join("generated.rs");
    fs::write(out, format!(
        "fn main() {{\n    let image = include_pnm::include_ppm!(\"{path}\");\n    println!(\"{{}}\", serde_json::json!({{\"height\": image.len(), \"width\": image[0].len(), \"rgb\": image}}));\n}}\n"
    )).unwrap();
}
