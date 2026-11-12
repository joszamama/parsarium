use std::error::Error;
use std::fs;
use std::io::{Cursor, Read};

fn output(name: &str, content: Option<&str>, size: u64) {
    println!("{}", serde_json::json!({"name": name, "content": content, "size": size}));
}

fn output_entry(name: &str, count: usize) {
    println!("{}", serde_json::json!({"name": name, "entry_count": count}));
}

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 3 {
        return Err("usage: parsarium-rust-zip PACKAGE CONTROL".into());
    }
    let bytes = fs::read(&args[2])?;
    match args[1].as_str() {
        "zip" => {
            let mut archive = zip::ZipArchive::new(Cursor::new(&bytes))?;
            let mut entry = archive.by_index(0)?;
            let name = entry.name()?.to_string();
            let size = entry.size();
            let mut content = String::new();
            entry.read_to_string(&mut content)?;
            output(&name, Some(&content), size);
        }
        "eazip" => {
            let mut archive = eazip::ArchiveReader::open(&args[2])?;
            let mut entry = archive.get_by_index(0).ok_or("no ZIP entry")?;
            let name = entry.metadata().name().to_string();
            let size = entry.metadata().uncompressed_size;
            let mut content = String::new();
            entry.read()?.read_to_string(&mut content)?;
            output(&name, Some(&content), size);
        }
        "rc-zip-sync" => {
            use rc_zip_sync::ReadZip;
            let archive = bytes.read_zip()?;
            let entry = archive.entries().next().ok_or("no ZIP entry")?;
            let name = entry.name.clone();
            let size = entry.uncompressed_size;
            let content = String::from_utf8(entry.bytes()?)?;
            output(&name, Some(&content), size);
        }
        "rawzip" => {
            let archive = rawzip::ZipArchive::from_slice(&bytes)?;
            let mut entries = archive.entries();
            let entry = entries.next_entry()?.ok_or("no ZIP entry")?;
            let normalized = entry.file_path().try_normalize()?;
            let name = normalized.as_ref().to_string();
            let size = entry.uncompressed_size_hint();
            let local = archive.get_entry(entry.wayfinder())?;
            let decoder = flate2::bufread::DeflateDecoder::new(local.data());
            let mut content = String::new();
            local.verifying_reader(decoder).read_to_string(&mut content)?;
            output(&name, Some(&content), size);
        }
        "tinyzip" => {
            let archive = tinyzip::Archive::try_from(fs::File::open(&args[2])?)?;
            let entry = archive.find_file(b"hello.txt")?;
            let mut name = [0_u8; 128];
            let name = String::from_utf8(entry.read_path(&mut name)?.to_vec())?;
            let size = entry.uncompressed_size();
            let mut content = String::new();
            match entry.compression()? {
                tinyzip::Compression::Deflated => {
                    flate2::read::DeflateDecoder::new(entry.reader()?).read_to_string(&mut content)?;
                }
                tinyzip::Compression::Stored => {
                    entry.reader()?.read_to_string(&mut content)?;
                }
            }
            output(&name, Some(&content), size);
        }
        "piz" => {
            let archive = piz::ZipArchive::new(&bytes)?;
            let entry = archive.entries().first().ok_or("no ZIP entry")?;
            let name = entry.path.to_string();
            let size = entry.size as u64;
            let mut content = String::new();
            archive.read(entry)?.read_to_string(&mut content)?;
            output(&name, Some(&content), size);
        }
        "zip_next" => {
            let mut archive = zip_next::ZipArchive::new(Cursor::new(&bytes))?;
            let mut entry = archive.by_index(0)?;
            let name = entry.name().to_string();
            let size = entry.size();
            let mut content = String::new();
            entry.read_to_string(&mut content)?;
            output(&name, Some(&content), size);
        }
        "zip-lzma" => {
            let mut archive = zip_lzma::ZipArchive::new(Cursor::new(&bytes))?;
            let mut entry = archive.by_index(0)?;
            let name = entry.name().to_string();
            let size = entry.size();
            let mut content = String::new();
            entry.read_to_string(&mut content)?;
            output(&name, Some(&content), size);
        }
        "zip-extract" => {
            let root = tempfile::tempdir()?;
            let destination = root.path().join("out");
            #[allow(deprecated)]
            zip_extract::extract(Cursor::new(&bytes), &destination, false)?;
            let entry = fs::read_dir(&destination)?.next().ok_or("no extracted ZIP entry")??;
            let name = entry.file_name().to_string_lossy().to_string();
            let content = fs::read_to_string(entry.path())?;
            output(&name, Some(&content), content.len() as u64);
        }
        "zip-extensions" => {
            let mut content = Vec::new();
            zip_extensions::inflate::zip_extract::zip_extract_file_to_memory(
                &args[2].clone().into(), &"hello.txt".into(), &mut content)?;
            let content = String::from_utf8(content)?;
            output("hello.txt", Some(&content), content.len() as u64);
        }
        "oxiarc-archive" => {
            let mut archive = oxiarc_archive::zip::read_zip(Cursor::new(&bytes))?;
            let entry = archive.entries().first().ok_or("no ZIP entry")?.clone();
            let content = String::from_utf8(archive.extract(&entry)?)?;
            output(&entry.name, Some(&content), entry.size);
        }
        "openpack" => {
            let archive = openpack::OpenPack::open_default(&args[2])?;
            let entry = archive.entries()?.into_iter().next().ok_or("no ZIP entry")?;
            let content = String::from_utf8(archive.read_entry(&entry.name)?)?;
            output(&entry.name, Some(&content), entry.uncompressed_size);
        }
        "s-zip" => {
            let mut archive = s_zip::StreamingZipReader::open(&args[2])?;
            let entry = archive.entries().first().ok_or("no ZIP entry")?.clone();
            let content = String::from_utf8(archive.read_entry_by_name(&entry.name)?)?;
            output(&entry.name, Some(&content), entry.uncompressed_size);
        }
        "archiver-rs" => {
            use archiver_rs::Archive;
            let mut archive = archiver_rs::Zip::new(Cursor::new(&bytes))?;
            let names = archive.files()?;
            let name = names.first().ok_or("no ZIP entry")?;
            output_entry(name, names.len());
        }
        "zip_structs" => {
            let header = zip_structs::zip_local_file_header::ZipLocalFileHeader
                ::read_and_generate_from_signature(&mut Cursor::new(&bytes))?;
            let name = String::from_utf8(header.file_name_raw)?;
            output(&name, None, header.uncompressed_size as u64);
        }
        "async_zip" => {
            #[allow(deprecated)]
            pollster::block_on(async {
                let reader = upstream_async_zip::base::read::mem::ZipFileReader::new(bytes).await?;
                let entry = reader.file().entries().first().ok_or("no ZIP entry")?;
                let name = entry.filename().as_str()?.to_string();
                let size = entry.uncompressed_size();
                let mut content = String::new();
                futures_lite::io::AsyncReadExt::read_to_string(
                    &mut reader.reader_with_entry(0).await?, &mut content).await?;
                output(&name, Some(&content), size);
                Ok::<(), Box<dyn Error>>(())
            })?;
        }
        "astral_async_zip" => {
            pollster::block_on(async {
                let reader = astral_async_zip::base::read::mem::ZipFileReader::new(bytes).await?;
                let entry = reader.file().entries().first().ok_or("no ZIP entry")?;
                let name = entry.filename().as_str()?.to_string();
                let size = entry.uncompressed_size();
                let mut content = String::new();
                futures_lite::io::AsyncReadExt::read_to_string(
                    &mut reader.reader_with_entry(0).await?, &mut content).await?;
                output(&name, Some(&content), size);
                Ok::<(), Box<dyn Error>>(())
            })?;
        }
        "archive-core" => {
            let mut archive = archive_core::Archive::open(&bytes, Some("hello.zip"))?
                .ok_or("ZIP archive not recognized")?;
            let entry = archive.entries().first().ok_or("no ZIP entry")?.clone();
            let content = String::from_utf8(archive.read(0)?)?;
            output(&entry.name, Some(&content), entry.size);
        }
        "zip-forensic-core" => {
            let mut archive = zip_core::ZipArchive::new(Cursor::new(&bytes))?;
            let name = archive.file_names().next().ok_or("no ZIP entry")?.to_string();
            let mut entry = archive.by_index(0)?;
            let size = entry.size();
            let mut content = String::new();
            entry.read_to_string(&mut content)?;
            output(&name, Some(&content), size);
        }
        "libarchive2" => {
            let mut archive = libarchive2::ReadArchive::open(&args[2])?;
            let entry = archive.next_entry()?.ok_or("no ZIP entry")?;
            let name = entry.pathname().ok_or("ZIP entry has no name")?;
            let size = entry.size() as u64;
            let content = String::from_utf8(archive.read_data_to_vec()?)?;
            output(&name, Some(&content), size);
        }
        other => return Err(format!("unknown ZIP package: {other}").into()),
    }
    Ok(())
}
