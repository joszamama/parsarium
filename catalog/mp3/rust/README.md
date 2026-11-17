# MP3 / Rust — pilot

**Status:** pilot_six_paths_search_bounded; incomplete. 6 verified third-party paths, 0 verified standard APIs, 6 verified Docker harnesses.

Six verified package paths cover four parser families on two valid untagged CBR controls: Symphonia's Rust MP3 demuxer/decoder, reached directly through symphonia-bundle-mp3 and through the symphonia facade's probe and codec registry; minimp3's C decoder through the Rust minimp3 binding and as the pure-Rust nanomp3 port; the mp3-duration frame-header scanner, which reports only a summed duration; rusty_mp3's in-house pure-Rust Layer III decoder. The symphonia facade is a separate package API over the same Symphonia family, not a new engine; nanomp3 is a separate package API over the minimp3 family (its minimp3-compatible PCM is byte-identical to scalar minimp3.h), and nanomp3-core, the decoder it re-exports, is counted only through nanomp3. Five leads remain unresolved, so the verified ranks are not a claim about all MP3 parsers. Search covers the first 100 hits of six crates.io queries (591 hits, 350 unique) captured 2026-11-17; the 'mp3' query alone reports 1119 matches. Recent downloads include transitive dependency pulls and are an adoption proxy, not evidence of direct MP3 parsing use. The two controls do not establish VBR, Xing/Info, free-format, Layer I/II or MPEG-2.5 support.

[Ranking and search limits](../../../data/rust/mp3/ranking.md) · [Standard API inventory](../../../data/rust/mp3/standard.json)

## Third-party parsers

- [symphonia](symphonia/README.md) — verified Docker harness
- [symphonia-bundle-mp3](symphonia-bundle-mp3/README.md) — verified Docker harness
- [minimp3](minimp3/README.md) — verified Docker harness
- [mp3-duration](mp3-duration/README.md) — verified Docker harness
- [rusty_mp3](rusty-mp3/README.md) — verified Docker harness
- [nanomp3](nanomp3/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
