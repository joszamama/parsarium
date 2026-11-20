use parsarium_mp3_id3_harness::parse;
use std::env;use std::fs;
fn main()->Result<(),Box<dyn std::error::Error>>{
 let path=env::args().nth(1).ok_or("expected control path")?;
 let p=parse(&fs::read(path)?)?;
 let mut out=serde_json::Map::new();
 for (key,value) in [("title",p.title),("artist",p.artist),("album",p.album)]{
  if let Some(text)=value{out.insert(key.to_owned(),serde_json::Value::String(text));}
 }
 println!("{}",serde_json::Value::Object(out));
 Ok(())
}
