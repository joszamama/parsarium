# RUST × MP3: selected parsers

6 control-verified third-party paths over four parser families; pilot scope. The ceiling is ten and the cell is not padded. Frame-level leads that have not yet been run are listed in [leads.json](leads.json).

## Primary within-cell adoption metric

crates.io recent downloads (90 days), from the search API in [registry-snapshot.json](registry-snapshot.json), captured 2026-11-17.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [symphonia](https://docs.rs/symphonia/0.6.1/symphonia/) | 0.6.1 | 11,469,426 | Untagged bytes probed with no extension hint (`mp3` feature enabled), every Layer III frame demuxed and decoded: probed format, codec, frames, frame bytes, sample rate, channels, decoded samples | Facade over the Symphonia MP3 demuxer and decoder; same family as rank 2, not an independent engine |
| 2 | [symphonia-bundle-mp3](https://docs.rs/symphonia-bundle-mp3/0.6.1/symphonia_bundle_mp3/) | 0.6.1 | 10,651,437 | Every Layer III frame demuxed and decoded: frames, frame bytes, sample rate, channels, decoded samples | Symphonia MP3 demuxer and decoder |
| 3 | [minimp3](https://docs.rs/minimp3/0.6.1/minimp3/) | 0.6.1 | 156,316 | Every frame decoded to PCM on two untagged CBR controls; headers, frames, samples and PCM hash | minimp3 C decoder via minimp3-sys Rust binding; shared underlying family with Go tosone/minimp3 and Rust nanomp3 |
| 4 | [mp3-duration](https://docs.rs/mp3-duration/0.1.10/mp3_duration/) | 0.1.10 | 149,042 | Every frame header walked to EOF; summed duration only (no frame count, decode or tags exposed) | Own MPEG frame-header scanner |
| 5 | [rusty_mp3](https://docs.rs/rusty_mp3/1.0.6/rusty_mp3/) | 1.0.6 | 81,660 | Every Layer III frame frame-synced and decoded to f32 PCM: frames, sample rate, channels, samples, PCM hash | In-house pure-Rust Layer III decoder; independent of Symphonia and minimp3 |
| 6 | [nanomp3](https://docs.rs/nanomp3/0.2.0/nanomp3/) | 0.2.0 | 51,847 | Every frame walked, whole buffer decoded to i16 PCM (default and minimp3-compatible): frames, frame bytes, sample rate, channels, bitrate, samples, PCM hashes | Pure-Rust port of minimp3 via nanomp3-core; shared family with rank 3, not an independent engine |

Unverified frame-level leads, by the same metric: minimp3_fixed 25,898, mp3-metadata 13,775, puremp3 11,921, rmp3 6,272, oxideav-mp3 5,356. Not counted separately: nanomp3-core 43,688 (the decoder nanomp3 re-exports; same family, counted once through nanomp3). Recent downloads include transitive dependency pulls. The two controls do not establish broad MP3 compatibility; the minimp3 source documentation warns about memory unsoundness in the binding. mp3-duration exposes only a duration, so its control result is checked through the header walk's frame count times per-frame duration.
