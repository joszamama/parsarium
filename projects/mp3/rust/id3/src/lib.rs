use std::io::Cursor;
use id3::TagLike;
#[derive(Debug,PartialEq,Eq)]
pub struct Parsed {pub title:Option<String>,pub artist:Option<String>,pub album:Option<String>}
pub fn parse(data:&[u8])->Result<Parsed,Box<dyn std::error::Error>>{
 if data.is_empty() || data.len()>(1<<20){return Err("input outside harness limit".into());}
 let tag=id3::Tag::read_from(Cursor::new(data))?;
 // A frame the tag does not have is reported as absent.
 Ok(Parsed{title:tag.title().map(str::to_owned),
           artist:tag.artist().map(str::to_owned),
           album:tag.album().map(str::to_owned)})
}
