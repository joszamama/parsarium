# RUST × MP3 with ID3v2: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

crates.io recent downloads (90 days).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
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

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
