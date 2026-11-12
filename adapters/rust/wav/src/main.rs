use std::error::Error;
use std::fs::File;
use std::path::Path;

#[allow(deprecated)] // The pinned wav 1.0.1 reader is deprecated but remains a qualifying release.
fn parse(package: &str, path: &Path) -> Result<serde_json::Value, Box<dyn Error>> {
    let (sample_rate, channels, samples): (u32, u16, usize) = match package {
        "hound" => {
            let mut reader = hound::WavReader::open(path)?;
            let spec = reader.spec();
            let values: Vec<i16> = reader.samples::<i16>().collect::<Result<_, _>>()?;
            assert_eq!(values, [0, 1000, -1000, 0]);
            (spec.sample_rate, spec.channels, values.len())
        }
        "wav" => {
            let (header, data) = wav::read(&mut File::open(path)?)?;
            let values = data.as_sixteen().ok_or("expected 16-bit PCM")?;
            assert_eq!(values, &[0, 1000, -1000, 0]);
            (header.sampling_rate, header.channel_count, values.len())
        }
        "wav_io" => {
            let (header, values) = wav_io::read_from_file(File::open(path)?)?;
            assert_eq!(values.len(), 4);
            (header.sample_rate, header.channels, values.len())
        }
        "riff-wave" => {
            let mut reader = riff_wave::WaveReader::new(File::open(path)?)?;
            let values: Vec<i16> = (0..4).map(|_| reader.read_sample_i16()).collect::<Result<_, _>>()?;
            assert_eq!(values, [0, 1000, -1000, 0]);
            (reader.pcm_format.sample_rate, reader.pcm_format.num_channels, values.len())
        }
        "wavers" => {
            let (values, sample_rate) = wavers::read::<i16, _>(path)?;
            assert_eq!(&*values, &[0, 1000, -1000, 0]);
            let reader = wavers::Wav::<i16>::from_path(path)?;
            (sample_rate as u32, reader.n_channels(), values.len())
        }
        "bwavfile" => {
            let mut reader = bwavfile::WaveReader::open(path)?;
            let format = reader.format()?;
            let frames = reader.frame_length()?;
            (format.sample_rate, format.channel_count, frames as usize * format.channel_count as usize)
        }
        "symphonia" => {
            use symphonia::core::formats::{FormatOptions, TrackType};
            use symphonia::core::formats::probe::Hint;
            use symphonia::core::io::MediaSourceStream;
            let source = MediaSourceStream::new(Box::new(File::open(path)?), Default::default());
            let mut hint = Hint::new();
            hint.with_extension("wav");
            let mut reader = symphonia::default::get_probe().probe(&hint, source, FormatOptions::default(), Default::default())?;
            let track = reader.default_track(TrackType::Audio).ok_or("no audio track")?;
            let params = track.codec_params.as_ref().ok_or("no codec parameters")?.audio().ok_or("not audio")?;
            let sample_rate = params.sample_rate.ok_or("no sample rate")?;
            let channels = params.channels.as_ref().ok_or("no channels")?.count() as u16;
            let frames = track.num_frames.ok_or("no frame count")?;
            assert!(reader.next_packet()?.is_some());
            (sample_rate, channels, frames as usize * channels as usize)
        }
        "symphonia-format-riff" => {
            use symphonia::core::formats::{FormatOptions, FormatReader, TrackType};
            use symphonia::core::io::MediaSourceStream;
            let source = MediaSourceStream::new(Box::new(File::open(path)?), Default::default());
            let mut reader = symphonia_format_riff::WavReader::try_new(source, FormatOptions::default())?;
            let track = reader.default_track(TrackType::Audio).ok_or("no audio track")?;
            let params = track.codec_params.as_ref().ok_or("no codec parameters")?.audio().ok_or("not audio")?;
            let sample_rate = params.sample_rate.ok_or("no sample rate")?;
            let channels = params.channels.as_ref().ok_or("no channels")?.count() as u16;
            let frames = track.num_frames.ok_or("no frame count")?;
            assert!(reader.next_packet()?.is_some());
            (sample_rate, channels, frames as usize * channels as usize)
        }
        "symphonium" => {
            let source = symphonium::probe_from_file(path, None)?;
            let sample_rate = source.sample_rate().ok_or("no sample rate")?.get();
            let track = source.format_reader().default_track(symphonia::core::formats::TrackType::Audio).ok_or("no audio track")?;
            let frames = track.num_frames.ok_or("no frame count")?;
            (sample_rate, source.num_channels().get() as u16, frames as usize * source.num_channels().get())
        }
        "audio-file" => {
            let audio = audio_file::read::<f32>(path, audio_file::ReadConfig::default())?;
            (audio.sample_rate, audio.num_channels, audio.samples_interleaved.len())
        }
        "waveadapter" => {
            let reader = waveadapter::WavReader::new(File::open(path)?)?;
            (reader.sample_rate() as u32, reader.channels() as u16, reader.frames() * reader.channels())
        }
        "ryf" => {
            let audio = ryf::read(path)?;
            (audio.sample_rate, audio.num_channels() as u16, audio.frames() * audio.num_channels())
        }
        "wav-codec" => {
            let mut reader = wav_codec::WavReader::open(path)?;
            let spec = reader.spec();
            let values: Vec<i16> = reader.samples::<i16>().collect::<Result<_, _>>()?;
            assert_eq!(values, [0, 1000, -1000, 0]);
            (spec.sample_rate, spec.channels, values.len())
        }
        "wave_stream" => {
            use wave_stream::open_wav::OpenWav;
            use wave_stream::wave_reader::RandomAccessOpenWavReader;
            let reader = wave_stream::read_wav_from_file_path(path)?;
            let rate = reader.sample_rate();
            let channels = reader.num_channels();
            let frames = reader.len_samples();
            assert!(reader.get_random_access_f32_reader()?.read_sample(0).is_ok());
            (rate, channels, frames * channels as usize)
        }
        "creak" => {
            let reader = creak::Decoder::open(path)?;
            let info = reader.info();
            let values: Vec<f32> = reader.into_samples()?.collect::<Result<_, _>>()?;
            (info.sample_rate(), info.channels() as u16, values.len())
        }
        "pure_wav" => {
            let data = std::fs::read(path)?;
            let mut parser = pure_wav::Parser::default();
            loop {
                let step = parser.read_instruction();
                let start = step.position as usize;
                let end = start + step.len as usize;
                match parser.process_data(&data[start..end]).map_err(|e| format!("{e:?}"))? {
                    pure_wav::ProcessDataOutput::Done(meta) => {
                        let channels = meta.fmt.n_channels.get();
                        let samples = meta.data_len as usize / (meta.fmt.w_bits_per_sample.get() as usize / 8);
                        break (meta.fmt.n_samples_per_sec.get(), channels, samples);
                    }
                    pure_wav::ProcessDataOutput::InProgress(next) => parser = next,
                }
            }
        }
        "symphonia-format-wav" => {
            use symphonia_core_05::formats::FormatReader;
            use symphonia_core_05::io::MediaSourceStream;
            let source = MediaSourceStream::new(Box::new(File::open(path)?), Default::default());
            #[allow(deprecated)]
            let mut reader = symphonia_format_wav::WavReader::try_new(source, &Default::default())?;
            let track = reader.tracks().first().ok_or("no audio track")?;
            let params = &track.codec_params;
            let sample_rate = params.sample_rate.ok_or("no sample rate")?;
            let channels = params.channels.ok_or("no channels")?.count() as u16;
            let frames = params.n_frames.ok_or("no frame count")?;
            assert!(reader.next_packet().is_ok());
            (sample_rate, channels, frames as usize * channels as usize)
        }
        "nwav" => {
            let bytes = std::fs::read(path)?;
            let wave = nwav::WAV::from_data(&bytes);
            let chunks = wave.available_chunks();
            assert!(chunks.iter().any(|chunk| chunk.name == "RIFF"));
            let fmt = match wave.read_chunk_by_name("fmt ").ok_or("no format chunk")? {
                nwav::Chunk::Format(fmt) => fmt,
                _ => return Err("unexpected format chunk".into()),
            };
            let data = match wave.read_chunk_by_name("data").ok_or("no data chunk")? {
                nwav::Chunk::Data(bytes) => bytes,
                _ => return Err("unexpected data chunk".into()),
            };
            (fmt.sampling_rate, fmt.number_of_channels, data.len() / (fmt.bits_per_sample as usize / 8))
        }
        "surge-hound" => {
            let mut reader = surge_hound::WavReader::open(path)?;
            let spec = reader.spec();
            let values: Vec<i16> = reader.samples::<i16>().collect::<Result<_, _>>()?;
            assert_eq!(values, [0, 1000, -1000, 0]);
            (spec.sample_rate, spec.channels, values.len())
        }
        "rff-format-wav" => {
            let mut registry = rff_format::FormatRegistry::new();
            rff_format_wav::register(&mut registry);
            let mut reader = registry.open_demuxer("wav", Box::new(File::open(path)?))?;
            let tracks = reader.read_header()?;
            let track = tracks.first().ok_or("no audio track")?;
            let sample_rate = track.sample_rate;
            let channels = track.channels;
            let packet = reader.read_packet()?;
            (sample_rate, channels, packet.duration as usize * channels as usize)
        }
        _ => return Err(format!("unknown package: {package}").into()),
    };
    Ok(serde_json::json!({"sample_rate": sample_rate, "channels": channels, "samples": samples}))
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = std::env::args().skip(1);
    let package = args.next().ok_or("usage: parsarium-rust-wav PACKAGE CONTROL")?;
    let path = args.next().ok_or("missing control path")?;
    if args.next().is_some() { return Err("unexpected extra argument".into()); }
    println!("{}", parse(&package, Path::new(&path))?);
    Ok(())
}
