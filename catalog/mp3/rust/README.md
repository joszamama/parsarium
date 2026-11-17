# MP3 / Rust — pilot

**Status:** pilot_one_path_search_bounded; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

Pilot cell: one verified path, chosen as the highest crates.io 90-day download count (10,651,437) among hits that contain an MPEG audio frame parser. The facade crate symphonia (11,469,426) ranks higher but re-exports the same family. 11 frame-level leads remain unverified, so the count of one reflects pilot scope, not a search result. Search covers only the first 100 hits of six queries (591 hits, 350 unique) captured 2026-11-17; the 'mp3' query alone reports 1119 matches. Recent downloads include transitive dependency pulls (Symphonia is a dependency of rodio and others) and are an adoption proxy, not evidence of direct MP3 parsing use. Two untagged CBR controls (MPEG-1 44.1 kHz mono, MPEG-2 22.05 kHz stereo) do not establish VBR, Xing/Info, free-format, Layer I/II, or MPEG-2.5 support.

[Ranking and search limits](../../../data/rust/mp3/ranking.md) · [Standard API inventory](../../../data/rust/mp3/standard.json)

## Third-party parsers

- [symphonia-bundle-mp3](symphonia-bundle-mp3/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
