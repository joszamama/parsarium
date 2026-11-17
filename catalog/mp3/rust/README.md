# MP3 / Rust — pilot

**Status:** pilot_two_paths_search_bounded; incomplete. 2 verified third-party paths, 0 verified standard APIs, 2 verified Docker harnesses.

Two independent parser families are verified on two valid untagged CBR controls: Symphonia's Rust MP3 demuxer/decoder and minimp3's C decoder through the Rust minimp3 binding. The higher-download symphonia facade re-exports the selected Symphonia family. Ten leads remain unresolved, so the verified ranks are not a claim about all MP3 parsers. Search covers the first 100 hits of six crates.io queries (591 hits, 350 unique) captured 2026-11-17; the 'mp3' query alone reports 1119 matches. Recent downloads include transitive dependency pulls and are an adoption proxy, not evidence of direct MP3 parsing use. The two controls do not establish VBR, Xing/Info, free-format, Layer I/II or MPEG-2.5 support.

[Ranking and search limits](../../../data/rust/mp3/ranking.md) · [Standard API inventory](../../../data/rust/mp3/standard.json)

## Third-party parsers

- [symphonia-bundle-mp3](symphonia-bundle-mp3/README.md) — verified Docker harness
- [minimp3](minimp3/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
