use std::io::Cursor;
use id3::TagLike;
#[derive(Debug,PartialEq,Eq)]
pub struct Parsed {pub title:String,pub artist:String,pub album:String}
pub fn parse(data:&[u8])->Result<Parsed,Box<dyn std::error::Error>>{
 if data.is_empty() || data.len()>(1<<20){return Err("input outside harness limit".into());}
 let tag=id3::Tag::read_from(Cursor::new(data))?;
 Ok(Parsed{title:tag.title().ok_or("missing title")?.to_owned(),
           artist:tag.artist().ok_or("missing artist")?.to_owned(),
           album:tag.album().ok_or("missing album")?.to_owned()})
}
