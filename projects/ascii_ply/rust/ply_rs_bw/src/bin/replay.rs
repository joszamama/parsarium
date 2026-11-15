use parsarium_ascii_ply_ply_rs_bw_harness::parse;
use std::env;use std::fs;
fn main()->Result<(),Box<dyn std::error::Error>>{
 let path=env::args().nth(1).ok_or("expected control path")?;
 let p=parse(&fs::read(path)?)?;
 println!("{}",serde_json::json!({"vertices":p.vertices,"faces":p.faces,"format":p.format}));
 Ok(())
}
