# RUST × MP3: selected parsers

3 control-verified third-party paths over two parser families; pilot scope. The ceiling is ten and the cell is not padded. Frame-level leads that have not yet been run are listed in [leads.json](leads.json).

## Primary within-cell adoption metric

crates.io recent downloads (90 days), from the search API in [registry-snapshot.json](registry-snapshot.json), captured 2026-11-17.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [symphonia](https://docs.rs/symphonia/0.6.1/symphonia/) | 0.6.1 | 11,469,426 | Untagged bytes probed with no extension hint (`mp3` feature enabled), every Layer III frame demuxed and decoded: probed format, codec, frames, frame bytes, sample rate, channels, decoded samples | Facade over the Symphonia MP3 demuxer and decoder; same family as rank 2, not an independent engine |
| 2 | [symphonia-bundle-mp3](https://docs.rs/symphonia-bundle-mp3/0.6.1/symphonia_bundle_mp3/) | 0.6.1 | 10,651,437 | Every Layer III frame demuxed and decoded: frames, frame bytes, sample rate, channels, decoded samples | Symphonia MP3 demuxer and decoder |
| 3 | [minimp3](https://docs.rs/minimp3/0.6.1/minimp3/) | 0.6.1 | 156,316 | Every frame decoded to PCM on two untagged CBR controls; headers, frames, samples and PCM hash | minimp3 C decoder via minimp3-sys Rust binding; shared underlying family with Go tosone/minimp3 |

Unverified frame-level leads, by the same metric: mp3-duration 149,042, rusty_mp3 81,660, nanomp3 51,847, nanomp3-core 43,688, minimp3_fixed 25,898, mp3-metadata 13,775, puremp3 11,921, rmp3 6,272, oxideav-mp3 5,356. Recent downloads include transitive dependency pulls. The two controls do not establish broad MP3 compatibility; the minimp3 source documentation warns about memory unsoundness in the binding.
