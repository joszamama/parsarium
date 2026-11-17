# MP3 / C++ — pilot

**Status:** pilot_one_verified_bounded_search; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

One verified path; no padding. Search is a substring match over all Homebrew formula names and descriptions for six queries, captured 2026-11-17; header-only C++ decoders and vcpkg/Conan packages were not searched. Homebrew installs measure demand for the whole TagLib distribution, mostly as a tag library, not use of its MPEG property API. TagLib parses frame headers and does not decode audio; for CBR streams without Xing/VBRI its duration comes from stream size and the first frame's bitrate. Two untagged CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, or MPEG-2.5 support.

[Ranking and search limits](../../../data/cpp/mp3/ranking.md) · [Standard API inventory](../../../data/cpp/mp3/standard.json)

## Third-party parsers

- [taglib](taglib/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
