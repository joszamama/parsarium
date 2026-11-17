# MP3 / Java

**Status:** Three verified third-party paths and no Java SE MP3 API. The search is bounded at ten selected paths; this cell has not reached that ceiling.

JCodec, MP3SPI, and JLayer parse and decode both untagged MPEG Layer III controls in pinned Docker images. MP3SPI uses its own Java Sound reader and converter, then soundlibs JLayer for frame decoding. It shares JLayer's decoder lineage, so the three paths represent two decoder families. deps.dev direct-dependent counts are comparable within Maven but count use of the whole package, not MP3-specific calls. The controls do not establish VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5, or ID3 behavior.

[Ranking and search limits](../../../data/java/mp3/ranking.md) · [Standard API inventory](../../../data/java/mp3/standard.json)

## Third-party parsers

- [jcodec](jcodec/README.md) — verified Docker harness
- [mp3spi](mp3spi/README.md) — verified Docker harness
- [jlayer](jlayer/README.md) — verified Docker harness

## Standard and runtime APIs

No MP3 reader is included in the tested Java SE 25 runtime. MP3SPI is a third-party Java Sound service.
