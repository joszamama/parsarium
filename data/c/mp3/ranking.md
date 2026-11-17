# C plain MP3 parser pilot

This pilot has two verified third-party paths from independent decoder
families. [`mpg123`](../../../projects/mp3/c/mpg123/README.md) 1.33.7 decoded
both untagged MPEG Layer III controls from memory through the libmpg123 feed API
(`mpg123_open_feed`, `mpg123_feed`, `mpg123_decode_frame`).
[`libmad`](../../../projects/mp3/c/libmad/README.md) 0.16.5 (Homebrew formula
`mad`) decoded the same controls through `mad_stream_buffer`,
`mad_frame_decode` and `mad_synth_frame`, with the 8-byte `MAD_BUFFER_GUARD`
zero padding its frame decoder requires and no recoverable errors.

Homebrew install-on-request counts come from the
[saved search snapshot](registry-snapshot.json). They count installs of whole
formulae (the mpg123 player is included); they are an adoption proxy, not a
count of programs that call the decoder. The libmpg123 engine is also counted
in the active C MP3-with-ID3v2 cell, and libmad is the decoder behind its SoX
path; these are separate plain-frame paths.

## Primary within-cell adoption metric

Homebrew install-on-request count (365 days, 2025-11-17 to 2026-11-17).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [mpg123](https://www.mpg123.de/api/group__mpg123__input.shtml) | 1.33.7 | 12,256 | Every Layer III frame fed from memory and decoded: sample rate, channels, layer, frames, decoded samples | libmpg123 MPEG audio decoder |
| 2 | [libmad](https://codeberg.org/tenacityteam/libmad/src/tag/0.16.5/include/mad.h.in) (`mad`) | 0.16.5 | 1,145 | Every Layer III frame buffered from memory, decoded and synthesized: sample rate, channels, layer, frames, decoded samples, bitrate range, recoverable errors, consumed bytes | libmad MPEG audio decoder |

## Leads

Seven Homebrew queries returned 28 hits and 24 distinct formulae. The
[leads](leads.json) record each one, plus two header-only decoders outside
Homebrew. None of these is a verified entry.

- lame 4.0 (6,992): HIP decoder built over libmpg123; same family, not run.
- libmp3splt 0.9.2 (102): decodes through libmad, so it shares the verified
  libmad family; not run.
- minimp3 and dr_mp3: not Homebrew formulae, so they have no primary value.
  GitHub stars (lieff/minimp3 1,988; mackron/dr_libs 1,901, shared by every
  dr_libs header) are supplemental and not compared with the table. dr_mp3 says
  it is based on minimp3. Both passed local technical checks (both controls,
  parser-source coverage, stable AFL++ feedback; dr_mp3 PCM is byte-identical
  to the Rust minimp3 receipt), but PROTOCOL.md allows a star fallback only in
  PLY cells, so neither is selected.
- 20 hits are excluded: command-line tools without a library input API, tag
  tools, encoders, and non-C or non-decoder packages.

This two-entry pilot is neither a top-ten ranking nor evidence that only two C
decoders exist. The [cell record](cell.json) gives the remaining uncertainty and
the [standard-library finding](standard.json).
