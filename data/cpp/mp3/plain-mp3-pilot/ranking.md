# C++ plain MP3 parser pilot

The only verified third-party path in this pilot is
[`taglib`](../../../projects/mp3/cpp/taglib/README.md) 2.3.2. Its documented
`TagLib::MPEG::File` constructor over a `TagLib::ByteVectorStream` scanned the
frame headers of both untagged MPEG Layer III controls from memory and reported
MPEG version, layer, sample rate, channels, bitrate and duration. The formula
has **4,118 Homebrew installs on request** over 365 days in the
[saved search snapshot](registry-snapshot.json). That counts installs of the
whole TagLib distribution, mostly used for tags; it is an adoption proxy, not a
count of programs that read MPEG properties. The same TagLib library is already
counted in the active C++ MP3-with-ID3v2 cell; this is a separate plain-frame
path, not an independent parser family.

## Primary within-cell adoption metric

Homebrew install-on-request count (365 days, 2025-11-17 to 2026-11-17).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [taglib](https://taglib.org/api/classTagLib_1_1MPEG_1_1File.html) | 2.3.2 | 4,118 | Layer III frame headers read from memory: version, layer, sample rate, channels, bitrate, duration | TagLib MPEG frame-header and tag parser |

| Control | Version | Layer | Sample rate | Channels | Bitrate | Duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `controls/mp3/tone-44k-mono.mp3` | MPEG-1 | 3 | 44,100 | 1 | 64 kbps | 287 ms |
| `controls/mp3/tone-22k-stereo.mp3` | MPEG-2 | 3 | 22,050 | 2 | 32 kbps | 314 ms |

TagLib reads headers and does not decode audio. Neither control has a
Xing/VBRI header, so TagLib takes the duration from stream size and the first
frame's bitrate: 2,298 bytes at 64 kbps is 287 ms, and 1,254 bytes at 32 kbps
is 314 ms. The frame walk in `controls/mp3/check_controls.py` gives
11 × 1,152 / 44,100 = 287 ms and 12 × 576 / 22,050 = 314 ms.

## Leads

Six Homebrew queries returned 31 hits and 25 distinct formulae. The
[leads](leads.json) record each one. None besides TagLib is a verified entry.

- mpg123 (12,256), lame (6,992), mad (1,145) and libmp3splt (102) are C
  libraries. libmpg123 is verified in the C plain MP3 cell; the others are
  listed there.
- mp3val, mp3check, mp3blaster, ncmdump and mp3fs are C++ programs with no
  documented library, byte or stream API. mp3unicode is a tag-only tool.
- The other hits are excluded: command-line tools without a library input API,
  tag tools, encoders, and non-C++ or non-parser packages.

This one-entry pilot is neither a top-ten ranking nor evidence that only one
C++ frame parser exists; header-only libraries and vcpkg/Conan were not
searched. The [cell record](cell.json) gives the remaining uncertainty and the
[standard-library finding](standard.json).
