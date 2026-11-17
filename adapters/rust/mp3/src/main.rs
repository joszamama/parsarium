use std::error::Error;
use std::fs::File;
use std::path::Path;

fn parse(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let result = match package {
        "id3" => {
            use id3::TagLike;
            let tag = id3::Tag::read_from_path(path)?;
            serde_json::json!({"title":tag.title(), "artist":tag.artist(), "album":tag.album()})
        }
        "lofty" => {
            use lofty::file::TaggedFileExt;
            use lofty::tag::Accessor;
            let file = lofty::read_from_path(path)?;
            let tag = file.primary_tag().ok_or("no primary tag")?;
            serde_json::json!({"title":tag.title(), "artist":tag.artist(), "album":tag.album()})
        }
        "minimp3" => {
            let mut decoder = minimp3::Decoder::new(File::open(path)?);
            let frame = decoder.next_frame()?;
            serde_json::json!({"sample_rate":frame.sample_rate,"channels":frame.channels,"decoded_samples":frame.data.len()})
        }
        "mp3-duration" => {
            let duration = mp3_duration::from_path(path)?;
            serde_json::json!({"duration_ms":duration.as_millis()})
        }
        "mp3-metadata" => {
            let meta = mp3_metadata::read_from_file(path).map_err(|error| format!("{error:?}"))?;
            let first = meta.frames.first().ok_or("no MP3 frame")?;
            serde_json::json!({"frames":meta.frames.len(),"sample_rate":first.sampling_freq})
        }
        "symphonia" => {
            use symphonia::core::formats::{FormatOptions, TrackType};
            use symphonia::core::formats::probe::Hint;
            use symphonia::core::io::MediaSourceStream;
            let source = MediaSourceStream::new(Box::new(File::open(path)?), Default::default());
            let mut hint = Hint::new();
            hint.with_extension("mp3");
            let mut reader = symphonia::default::get_probe().probe(&hint, source, FormatOptions::default(), Default::default())?;
            let track = reader.default_track(TrackType::Audio).ok_or("no audio track")?;
            let params = track.codec_params.as_ref().ok_or("no codec parameters")?.audio().ok_or("not audio")?;
            let sample_rate = params.sample_rate.ok_or("no sample rate")?;
            let channels = params.channels.as_ref().ok_or("no channels")?.count();
            let packet = reader.next_packet()?.ok_or("no audio packet")?;
            serde_json::json!({"sample_rate":sample_rate,"channels":channels,"packet_bytes":packet.data.len()})
        }
        "audiotags" => {
            let tag = audiotags::Tag::new().read_from_path(path)?;
            serde_json::json!({"title":tag.title(),"artist":tag.artist(),"album":tag.album().map(|album| album.title.to_owned())})
        }
        "puremp3" => {
            let (header, mut samples) = puremp3::read_mp3(File::open(path)?)?;
            let _ = samples.next().ok_or("no decoded sample")?;
            serde_json::json!({"sample_rate":header.sample_rate.hz(),"channels":header.channels.num_channels()})
        }
        "symphonium" => {
            let source = symphonium::probe_from_file(path, None)?;
            serde_json::json!({"sample_rate":source.sample_rate().ok_or("no sample rate")?.get(),"channels":source.num_channels().get()})
        }
        "audio-file" => {
            let audio = audio_file::read::<f32>(path, audio_file::ReadConfig::default())?;
            serde_json::json!({"sample_rate":audio.sample_rate,"channels":audio.num_channels,"samples":audio.samples_interleaved.len()})
        }
        "minimp3_fixed" => {
            let mut decoder = minimp3_fixed::Decoder::new(File::open(path)?);
            let frame = decoder.next_frame()?;
            serde_json::json!({"sample_rate":frame.sample_rate,"channels":frame.channels,"decoded_samples":frame.data.len()})
        }
        "nanomp3" => {
            let bytes = std::fs::read(path)?;
            let audio = nanomp3::decode_all::<i16>(&bytes);
            if audio.samples.is_empty() { return Err("no decoded samples".into()); }
            serde_json::json!({"sample_rate":audio.sample_rate,"layer":audio.layer,"samples":audio.samples.len()})
        }
        "creak" => {
            let decoder = creak::Decoder::open(path)?;
            let info = decoder.info();
            let first = decoder.into_samples()?.next().ok_or("no decoded sample")??;
            serde_json::json!({"sample_rate":info.sample_rate(),"channels":info.channels(),"first_sample":first})
        }
        "moosicbox_audiotags" => {
            let tag = moosicbox_audiotags::Tag::new().read_from_path(path)?;
            serde_json::json!({"title":tag.title(),"artist":tag.artist()})
        }
        "symphonia-metadata" => {
            use symphonia::core::io::MediaSourceStream;
            use symphonia::core::meta::MetadataReader;
            let source = MediaSourceStream::new(Box::new(File::open(path)?), Default::default());
            let mut reader = symphonia_metadata::id3v2::Id3v2Reader::try_new(source, Default::default())?;
            let tags = reader.read_all()?.revision.media.tags;
            serde_json::json!({"tag_count":tags.len(),"keys":tags.iter().map(|tag| tag.raw.key.as_str()).collect::<Vec<_>>()})
        }
        "symphonia-bundle-mp3" => {
            use symphonia::core::formats::{FormatOptions, FormatReader, TrackType};
            use symphonia::core::io::MediaSourceStream;
            let bytes = std::fs::read(path)?;
            let id3_len = ((bytes[6] as usize) << 21) | ((bytes[7] as usize) << 14) | ((bytes[8] as usize) << 7) | bytes[9] as usize;
            let audio = bytes[10 + id3_len..].to_vec();
            let source = MediaSourceStream::new(Box::new(std::io::Cursor::new(audio)), Default::default());
            let mut reader = symphonia_bundle_mp3::MpaReader::try_new(source, FormatOptions::default())?;
            let track = reader.default_track(TrackType::Audio).ok_or("no audio track")?;
            let params = track.codec_params.as_ref().ok_or("no codec parameters")?.audio().ok_or("not audio")?;
            let sample_rate = params.sample_rate.ok_or("no sample rate")?;
            let channels = params.channels.as_ref().ok_or("no channels")?.count();
            let packet = reader.next_packet()?.ok_or("no audio packet")?;
            serde_json::json!({"sample_rate":sample_rate,"channels":channels,"packet_bytes":packet.data.len()})
        }
        "rmp3" => {
            let bytes = std::fs::read(path)?;
            let mut reader = rmp3::Decoder::new(&bytes);
            let audio = loop {
                match reader.next() {
                    Some(rmp3::Frame::Audio(audio)) => break (audio.sample_rate(),audio.channels(),audio.sample_count()),
                    Some(rmp3::Frame::Other(_)) => continue,
                    None => return Err("no audio frame".into()),
                }
            };
            serde_json::json!({"sample_rate":audio.0,"channels":audio.1,"samples_per_channel":audio.2})
        }
        "rusty_mp3" => {
            let bytes = std::fs::read(path)?;
            let mut decoder = rusty_mp3::Mp3Decoder::new();
            decoder.push(&bytes);
            let frame = decoder.next_frame()?;
            serde_json::json!({"sample_rate":frame.sample_rate,"channels":frame.channels,"decoded_samples":frame.samples.len()})
        }
        "oxideav-id3" => {
            let bytes = std::fs::read(path)?;
            let (tag, consumed) = oxideav_id3::parse_tag(&bytes)?;
            serde_json::json!({"version":format!("{:?}",tag.version),"frame_count":tag.frames.len(),"tag_bytes":consumed})
        }
        "id3-core" => {
            let bytes = std::fs::read(path)?;
            let tag = id3_core::Tag::parse(&bytes)?;
            serde_json::json!({"version":tag.major_version,"title":tag.text_field(id3_core::TextField::Title),"artist":tag.text_field(id3_core::TextField::Artist)})
        }
        _ => return Err(format!("unknown package: {package}").into()),
    };
    Ok(result)
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = std::env::args().skip(1);
    let package = args.next().ok_or("usage: parsarium-rust-mp3-id3v2 PACKAGE CONTROL")?;
    let path = args.next().ok_or("missing control path")?;
    if args.next().is_some() { return Err("unexpected extra argument".into()); }
    println!("{}", parse(&package, Path::new(&path))?);
    Ok(())
}
