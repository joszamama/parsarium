use std::io::Cursor;
#[derive(Debug, PartialEq, Eq)]
pub struct Parsed {pub vertices: usize,pub faces: usize,pub format: String}
pub fn parse(data: &[u8]) -> Result<Parsed, Box<dyn std::error::Error>> {
 if data.is_empty() || data.len() > (1<<20){return Err("input outside harness limit".into());}
 let parser=ply_rs_bw::parser::Parser::<ply_rs_bw::ply::DefaultElement>::new();
 let ply=parser.read_ply(&mut Cursor::new(data))?;
 Ok(Parsed{vertices:ply.payload.get("vertex").map_or(0,Vec::len),
           faces:ply.payload.get("face").map_or(0,Vec::len),
           format:format!("{:?}",ply.header.encoding)})
}
