use std::error::Error;
use std::fs::File;
use std::path::Path;

fn parse(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let result = match package {
        "mp4" => {
            let movie = mp4::read_mp4(File::open(path)?)?;
            serde_json::json!({"tracks":movie.tracks().len()})
        }
        "mp4parse" => {
            let movie = mp4parse::read_mp4(&mut File::open(path)?)?;
            serde_json::json!({"tracks":movie.tracks.len()})
        }
        "re_mp4" => {
            let (movie, _) = re_mp4::Mp4::read_file(path)?;
            serde_json::json!({"tracks":movie.tracks().len()})
        }
        "lofty" => {
            use lofty::file::TaggedFileExt;
            use lofty::tag::Accessor;
            let file = lofty::read_from_path(path)?;
            let tag = file.primary_tag().ok_or("no primary tag")?;
            serde_json::json!({"title":tag.title()})
        }
        "mp4-atom" => {
            use mp4_atom::ReadFrom;
            let ftyp = mp4_atom::Ftyp::read_from(&mut File::open(path)?)?;
            serde_json::json!({"major_brand":format!("{:?}",ftyp.major_brand),"compatible_brands":ftyp.compatible_brands.len()})
        }
        "mp4ameta" => {
            let tag = mp4ameta::Tag::read_from_path(path)?;
            serde_json::json!({"title":tag.title()})
        }
        "symphonia" => {
            use symphonia::core::formats::{FormatOptions, TrackType};
            use symphonia::core::formats::probe::Hint;
            use symphonia::core::io::MediaSourceStream;
            let source = MediaSourceStream::new(Box::new(File::open(path)?), Default::default());
            let mut hint = Hint::new();
            hint.with_extension("mp4");
            let mut movie = symphonia::default::get_probe().probe(&hint, source, FormatOptions::default(), Default::default())?;
            let track = movie.default_track(TrackType::Audio).ok_or("no audio track")?;
            let params = track.codec_params.as_ref().ok_or("no codec parameters")?.audio().ok_or("not audio")?;
            let sample_rate = params.sample_rate.ok_or("no sample rate")?;
            let packet = movie.next_packet()?.ok_or("no audio packet")?;
            serde_json::json!({"sample_rate":sample_rate,"packet_bytes":packet.data.len()})
        }
        "symphonia-format-isomp4" => {
            use symphonia::core::formats::{FormatOptions, FormatReader, TrackType};
            use symphonia::core::io::{MediaSourceStream, ReadBytes};
            let mut source = MediaSourceStream::new(Box::new(File::open(path)?), Default::default());
            source.read_quad_bytes()?;
            let mut movie = symphonia_format_isomp4::IsoMp4Reader::try_new(source, FormatOptions::default())?;
            let track = movie.default_track(TrackType::Audio).ok_or("no audio track")?;
            let params = track.codec_params.as_ref().ok_or("no codec parameters")?.audio().ok_or("not audio")?;
            let sample_rate = params.sample_rate.ok_or("no sample rate")?;
            let packet = movie.next_packet()?.ok_or("no audio packet")?;
            serde_json::json!({"sample_rate":sample_rate,"packet_bytes":packet.data.len()})
        }
        "mp4box" => {
            let mut file = File::open(path)?;
            let len = file.metadata()?.len();
            let boxes = mp4box::get_boxes(&mut file, len, true)?;
            serde_json::json!({"top_boxes":boxes.len(),"has_moov":boxes.iter().any(|b| b.typ == "moov")})
        }
        "mp4io" => {
            let bytes = std::fs::read(path)?;
            let movie = mp4io::Mp4::parse(&bytes)?;
            serde_json::json!({"tracks":movie.tracks().len()})
        }
        "mp4-core" => {
            let bytes = std::fs::read(path)?;
            let movie = mp4_core::Mp4File::parse(&bytes)?;
            if movie.file_type.is_none() || movie.movie.is_none() { return Err("missing file type or movie".into()); }
            serde_json::json!({"tracks":movie.tracks.len()})
        }
        "mp4-track" => {
            let movie = mp4_track::Mp4Reader::open(File::open(path)?)?;
            serde_json::json!({"tracks":movie.tracks().len()})
        }
        "mp4parse-patched" => {
            let movie = mp4parse_patched::read_mp4(&mut File::open(path)?, mp4parse_patched::ParseStrictness::Normal)?;
            serde_json::json!({"tracks":movie.tracks.len()})
        }
        "audio-file" => {
            let audio = audio_file::read::<f32>(path, audio_file::ReadConfig::default())?;
            serde_json::json!({"sample_rate":audio.sample_rate,"channels":audio.num_channels,"samples":audio.samples_interleaved.len()})
        }
        "rockbox-metadata" => {
            let metadata = rockbox_metadata::read(path)?;
            serde_json::json!({"title":metadata.title,"sample_rate":metadata.sample_rate})
        }
        "mp4san" => {
            let sanitized = mp4san::sanitize(File::open(path)?)?;
            serde_json::json!({"media_data_bytes":sanitized.data.len})
        }
        "rff-format-mp4" => {
            let mut formats = rff_format::FormatRegistry::new();
            rff_format_mp4::register(&mut formats);
            let mut demuxer = formats.open_demuxer("mp4", Box::new(File::open(path)?))?;
            let streams = demuxer.read_header()?;
            serde_json::json!({"streams":streams.len()})
        }
        "oxideav-mp4" => {
            use oxideav_core::{ReadSeek, RuntimeContext};
            let mut context = RuntimeContext::new();
            oxideav_mp4::register(&mut context);
            let input: Box<dyn ReadSeek> = Box::new(File::open(path)?);
            let demuxer = context.containers.open_demuxer("mp4", input, &context.codecs)?;
            serde_json::json!({"streams":demuxer.streams().len()})
        }
        "vsd-mp4" => {
            use std::cell::Cell;
            use std::rc::Rc;
            let timescale = Rc::new(Cell::new(None));
            let callback_timescale = Rc::clone(&timescale);
            let mut parser = vsd_mp4::Mp4Parser::new()
                .base_box("moov", vsd_mp4::children)
                .full_box("mvhd", move |mut movie| {
                    if movie.version == Some(0) {
                        movie.reader.skip(8)?;
                        callback_timescale.set(Some(movie.reader.read_u32()?));
                    }
                    Ok(())
                });
            parser.parse(&std::fs::read(path)?, false, false)?;
            serde_json::json!({"movie_timescale":timescale.get().ok_or("no mvhd timescale")?})
        }
        "revelo-parsers-container" => {
            use revelo_core::stream::StreamKind;
            let bytes = std::fs::read(path)?;
            let mut analysis = revelo_core::FileAnalyze::new(&bytes);
            let recognized = revelo_parsers_container::parse_mp4(&mut analysis);
            if !recognized { return Err("MP4 parser did not recognize control".into()); }
            serde_json::json!({"video_streams":analysis.stream_count(StreamKind::Video),"audio_streams":analysis.stream_count(StreamKind::Audio)})
        }
        "shiguredo_mp4" => {
            use shiguredo_mp4::Decode;
            let bytes = std::fs::read(path)?;
            let (file, consumed): (shiguredo_mp4::Mp4File, usize) = shiguredo_mp4::Mp4File::decode(&bytes)?;
            serde_json::json!({"top_boxes":file.boxes.len()+1,"consumed_bytes":consumed})
        }
        _ => return Err(format!("unknown package: {package}").into()),
    };
    Ok(result)
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = std::env::args_os().skip(1);
    let package = args.next().ok_or("usage: adapter PACKAGE CONTROL")?;
    let path = args.next().ok_or("usage: adapter PACKAGE CONTROL")?;
    if args.next().is_some() { return Err("usage: adapter PACKAGE CONTROL".into()); }
    let package = package.to_str().ok_or("package must be UTF-8")?;
    println!("{}", parse(package, Path::new(&path))?);
    Ok(())
}
