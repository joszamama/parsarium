# C plain MP3 parser pilot

The only verified third-party path in this pilot is
[`mpg123`](../../../projects/mp3/c/mpg123/README.md) 1.33.7. Its documented
libmpg123 feed API (`mpg123_open_feed`, `mpg123_feed`, `mpg123_decode_frame`)
decoded both untagged MPEG Layer III controls from memory. The formula has
**12,256 Homebrew installs on request** over 365 days in the
[saved search snapshot](registry-snapshot.json). That counts installs of the
whole mpg123 distribution, player included; it is an adoption proxy, not a
count of programs that call the decoder. The same libmpg123 engine is already
counted in the active C MP3-with-ID3v2 cell; this is a separate plain-frame
path, not an independent parser family.

## Primary within-cell adoption metric

Homebrew install-on-request count (365 days, 2025-11-17 to 2026-11-17).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [mpg123](https://www.mpg123.de/api/group__mpg123__input.shtml) | 1.33.7 | 12,256 | Every Layer III frame fed from memory and decoded: sample rate, channels, layer, frames, decoded samples | libmpg123 MPEG audio decoder |

## Leads

Seven Homebrew queries returned 28 hits and 24 distinct formulae. The
[leads](leads.json) record each one, plus two header-only decoders outside
Homebrew. None of these is a verified entry.

- lame 4.0 (6,992): HIP decoder built over libmpg123; same family, not run.
- mad 0.16.5 (1,145): libmad, an independent decoder; unresolved, not run.
- libmp3splt 0.9.2 (102): decodes through libmad; unresolved, not run.
- minimp3 and dr_mp3: not Homebrew formulae, so they have no primary value.
  GitHub stars (lieff/minimp3 1,988; mackron/dr_libs 1,901, shared by every
  dr_libs header) are supplemental and not compared with the table. dr_mp3 says
  it is based on minimp3.
- 20 hits are excluded: command-line tools without a library input API, tag
  tools, encoders, and non-C or non-decoder packages.

This one-entry pilot is neither a top-ten ranking nor evidence that only one C
decoder exists. The [cell record](cell.json) gives the remaining uncertainty and
the [standard-library finding](standard.json).
