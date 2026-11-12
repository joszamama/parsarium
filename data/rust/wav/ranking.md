# Rust × WAV: verified parser ranking

20 verified third-party crate paths; working goal 20, original ceiling 30. The metric is crates.io crate-level recent downloads over 90 days, captured at 2026-11-12T01:05:07.326671+00:00. It includes all releases of each crate name and is compared only within Rust. 0 crate(s) lack a metric and remain unranked; equal counts share a rank.

Search hits, unresolved leads, and the standard-library inventory are separate from this ranking. See `cell.json`, `leads.json`, and `verification.json` in this directory.

| Rank | Crate | Pinned release | 90-day downloads | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [symphonia](https://docs.rs/symphonia/0.6.1/symphonia/) | 0.6.1 | 11,081,825 | WAV track metadata and audio packet | Symphonia WAV demuxer |
| 2 | [symphonia-format-riff](https://docs.rs/symphonia-format-riff/0.6.1/symphonia_format_riff/) | 0.6.1 | 9,031,513 | WAV track metadata and audio packet | Symphonia WAV demuxer |
| 3 | [hound](https://docs.rs/hound/3.5.1/hound/) | 3.5.1 | 6,597,798 | Decoded PCM sample values and WAV metadata | Hound WAV reader |
| 4 | [wav](https://docs.rs/wav/1.0.1/wav/) | 1.0.1 | 52,996 | Decoded PCM sample values and WAV metadata | wav legacy reader |
| 5 | [symphonium](https://docs.rs/symphonium/0.13.0/symphonium/) | 0.13.0 | 30,932 | WAV track metadata and declared frames | Symphonia WAV demuxer |
| 6 | [riff-wave](https://docs.rs/riff-wave/0.1.3/riff_wave/) | 0.1.3 | 27,062 | Decoded PCM sample values and WAV metadata | riff-wave reader |
| 7 | [symphonia-format-wav](https://docs.rs/symphonia-format-wav/0.5.5/symphonia_format_wav/) | 0.5.5 | 20,023 | WAV track metadata and audio packet | Symphonia WAV demuxer (0.5 lineage) |
| 8 | [audio-file](https://docs.rs/audio-file/0.5.1/audio_file/) | 0.5.1 | 11,692 | Decoded PCM sample count and WAV metadata | audio-file native WAV reader |
| 9 | [wavers](https://docs.rs/wavers/1.5.1/wavers/) | 1.5.1 | 11,071 | Decoded PCM sample values and WAV metadata | wavers reader |
| 10 | [waveadapter](https://docs.rs/waveadapter/0.3.1/waveadapter/) | 0.3.1 | 10,707 | WAV metadata and declared frame length | waveadapter reader |
| 11 | [ryf](https://docs.rs/ryf/0.7.4/ryf/) | 0.7.4 | 7,228 | Decoded PCM frame count and WAV metadata | ryf WAVE demuxer |
| 12 | [bwavfile](https://docs.rs/bwavfile/2.0.1/bwavfile/) | 2.0.1 | 3,369 | WAV format and declared frame length | bwavfile reader |
| 13 | [wav_io](https://docs.rs/wav_io/0.1.17/wav_io/) | 0.1.17 | 2,715 | PCM sample count and WAV metadata | wav_io reader |
| 14 | [rff-format-wav](https://docs.rs/rff-format-wav/0.4.6/rff_format_wav/) | 0.4.6 | 1,660 | WAV track metadata and audio packet | Remade FFmpeg WAV demuxer |
| 15 | [pure_wav](https://docs.rs/pure_wav/2.0.0/pure_wav/) | 2.0.0 | 566 | WAV fmt/data chunks and declared sample count | pure_wav parser |
| 16 | [wav-codec](https://docs.rs/wav-codec/0.1.0/wav_codec/) | 0.1.0 | 512 | Decoded PCM sample values and WAV metadata | wav-codec reader |
| 17 | [creak](https://docs.rs/creak/0.3.0/creak/) | 0.3.0 | 326 | Decoded PCM sample count and WAV metadata | Hound WAV reader |
| 18 | [wave_stream](https://docs.rs/wave_stream/0.6.0/wave_stream/) | 0.6.0 | 188 | WAV metadata and first decoded sample | wave_stream reader |
| 19 | [surge-hound](https://docs.rs/surge-hound/0.2.11-alpha.0/surge_hound/) | 0.2.11-alpha.0 | 186 | Decoded PCM sample values and WAV metadata | Hound fork (surge-hound) |
| 20 | [nwav](https://docs.rs/nwav/0.1.2/nwav/) | 0.1.2 | 36 | WAV fmt/data chunks and declared sample count | nwav chunk reader |
