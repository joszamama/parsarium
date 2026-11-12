# Rust × MP3 with ID3v2: verified parser ranking

20 verified third-party crate paths; working goal 20, original ceiling 30. The metric is crates.io crate-level recent downloads over 90 days, captured at 2026-11-12T01:15:01.164806+00:00. It includes all releases of each crate name and is compared only within Rust. 0 crate(s) lack a metric and remain unranked; equal counts share a rank.

Search hits, unresolved leads, and the standard-library inventory are separate from this ranking. See `cell.json`, `leads.json`, and `verification.json` in this directory.

| Rank | Crate | Pinned release | 90-day downloads | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [symphonia-metadata](https://docs.rs/symphonia-metadata/0.6.1/symphonia_metadata/) | 0.6.1 | 11,287,777 | ID3v2 frame keys | Symphonia ID3v2 reader |
| 2 | [symphonia](https://docs.rs/symphonia/0.6.1/symphonia/) | 0.6.1 | 11,081,825 | MP3 track header and audio packet | Symphonia MP3 demuxer |
| 3 | [symphonia-bundle-mp3](https://docs.rs/symphonia-bundle-mp3/0.6.1/symphonia_bundle_mp3/) | 0.6.1 | 10,337,517 | MPEG Layer III track header and audio packet; adapter skips ID3v2 prefix before passing the stream | Symphonia MP3 demuxer |
| 4 | [id3](https://docs.rs/id3/1.17.3/id3/) | 1.17.3 | 1,655,284 | ID3v2 title, artist, album | id3 tag parser |
| 5 | [lofty](https://docs.rs/lofty/0.25.5/lofty/) | 0.25.5 | 677,609 | ID3v2 title, artist, album | Lofty MPEG/ID3 parser |
| 6 | [minimp3](https://docs.rs/minimp3/0.6.1/minimp3/) | 0.6.1 | 156,734 | Decoded first MPEG Layer III frame | minimp3 C decoder |
| 7 | [mp3-duration](https://docs.rs/mp3-duration/0.1.10/mp3_duration/) | 0.1.10 | 150,661 | MP3 frame-derived duration | mp3-duration frame scanner |
| 8 | [rusty_mp3](https://docs.rs/rusty_mp3/1.0.5/rusty_mp3/) | 1.0.5 | 66,835 | Decoded first MPEG Layer III frame | rusty_mp3 decoder |
| 9 | [nanomp3](https://docs.rs/nanomp3/0.2.0/nanomp3/) | 0.2.0 | 40,169 | Decoded MP3 samples and layer | nanomp3 decoder |
| 10 | [symphonium](https://docs.rs/symphonium/0.13.0/symphonium/) | 0.13.0 | 30,932 | MP3 track header | Symphonia MP3 demuxer |
| 11 | [minimp3_fixed](https://docs.rs/minimp3_fixed/0.5.4/minimp3_fixed/) | 0.5.4 | 25,567 | Decoded first MPEG Layer III frame | minimp3 C decoder |
| 12 | [moosicbox_audiotags](https://docs.rs/moosicbox_audiotags/0.1.0/moosicbox_audiotags/) | 0.1.0 | 19,756 | ID3v2 title and artist | moosicbox_audiotags via id3 |
| 13 | [mp3-metadata](https://docs.rs/mp3-metadata/0.4.0/mp3_metadata/) | 0.4.0 | 12,857 | MPEG frame count and sample rate | mp3-metadata parser |
| 14 | [audio-file](https://docs.rs/audio-file/0.5.1/audio_file/) | 0.5.1 | 11,692 | Decoded MP3 audio samples | audio-file via Symphonia |
| 15 | [puremp3](https://docs.rs/puremp3/0.1.0/puremp3/) | 0.1.0 | 10,544 | Decoded MP3 sample and frame header | puremp3 decoder |
| 16 | [audiotags](https://docs.rs/audiotags/0.5.0/audiotags/) | 0.5.0 | 9,213 | ID3v2 title, artist, album | audiotags via id3 |
| 17 | [rmp3](https://docs.rs/rmp3/0.3.1/rmp3/) | 0.3.1 | 5,848 | Decoded first MPEG Layer III frame | minimp3 C decoder |
| 18 | [oxideav-id3](https://docs.rs/oxideav-id3/0.0.7/oxideav_id3/) | 0.0.7 | 2,978 | ID3v2 version, frame count, consumed bytes | oxideav ID3 reader |
| 19 | [id3-core](https://docs.rs/id3-core/0.3.1/id3_core/) | 0.3.1 | 946 | ID3v2 version, title, artist | id3-core tag parser |
| 20 | [creak](https://docs.rs/creak/0.3.0/creak/) | 0.3.0 | 326 | MP3 audio header and first decoded sample | minimp3 C decoder |
