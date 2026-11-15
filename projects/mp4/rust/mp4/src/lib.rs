use std::fs::{self, File, OpenOptions};
use std::io::Write;
use std::sync::atomic::{AtomicU64, Ordering};
static NEXT: AtomicU64 = AtomicU64::new(0);
#[derive(Debug,PartialEq,Eq)]
pub struct Parsed {pub tracks:usize}
pub fn parse(data:&[u8])->Result<Parsed,Box<dyn std::error::Error>>{
 if data.is_empty() || data.len()>(1<<20){return Err("input outside harness limit".into());}
 let path=format!("/tmp/parsarium-mp4-{}-{}",std::process::id(),NEXT.fetch_add(1,Ordering::Relaxed));
 let mut file=OpenOptions::new().write(true).create_new(true).open(&path)?;
 let result=(||{
  file.write_all(data)?;drop(file);
  let movie=mp4::read_mp4(File::open(&path)?)?;
  Ok::<_,Box<dyn std::error::Error>>(Parsed{tracks:movie.tracks().len()})
 })();
 fs::remove_file(&path)?;
 result
}
