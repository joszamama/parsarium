use parsarium_mp3_id3_harness::parse;
use std::env;use std::fs;
fn main()->Result<(),Box<dyn std::error::Error>>{
 let path=env::args().nth(1).ok_or("expected control path")?;
 let p=parse(&fs::read(path)?)?;
 println!("{}",serde_json::json!({"title":p.title,"artist":p.artist,"album":p.album}));
 Ok(())
}
