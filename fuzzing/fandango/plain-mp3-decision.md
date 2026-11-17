# Why `-F mp3` is not a plain MP3 generator

The plain MP3 pilot tests contiguous MPEG Audio **Layer III** frames without
ID3 tags. Fanbase's [MP3 grammar](https://github.com/fandango-fuzzer/fanbase/blob/main/specs/mp3/mp3/mp3.fan)
(installed `mp3.fan` SHA-256
`686fd83716aee495f75c1ad788cb3c7cdc423fd91fb8d0fe8e1165d0c1caf1f5`)
always emits an ID3v2.3 prefix, eleven audio frames, and an ID3v1 trailer.
Its fixed audio sequence includes a **Layer II** frame and a **Layer I** frame.
Removing only the two tags therefore produces a mixed-layer stream, not the
plain Layer III input defined by this pilot.

## Fixed-control reproduction

Fandango 1.3.1 with `fuzz -F mp3 -n 1 --random-seed 7` and
`PYTHONHASHSEED=7` produced a 4,538-byte file, SHA-256
`7ef93f3b6fe2db9435bffd92298dcef7b4fb2d4bef2fc623c142dc365172ec72`.
The ID3v2 header declares a 64-byte prefix; the final 128 bytes start with
`TAG`. Removing exactly those ranges gives 4,346 bytes, SHA-256
`d2d5f555824a7a58120b189e69a60fa22e2da82ab62170642217d02d75c10f69`.
The frame headers at offsets 2,467 and 2,884 in the stripped file declare
Layer II and Layer I. The other nine are Layer III. The same stripped SHA was
observed from a separate 4,571-byte Fanbase output because the grammar keeps
the audio frame bytes fixed while varying tag text.

`ffprobe` identifies the stripped file as MP3 from its first frames. The
format-aware parsers give the decisive check: the pinned Go `go-mp3` adapter
exits with `mp3: only layer3 (want 1; got 2) is supported`, and the pinned Rust
Symphonia `/work/replay` exits with `invalid audio buffer signal spec`. The
public one-input fuzz bridges can exit successfully after swallowing a parser
error, so their exit status alone does not verify this file.

The command `parsarium fandango generate mp3 ...` therefore has no default
Fanbase route. A custom `--spec FILE.fan` must generate a contiguous Layer III
stream and be checked by a format-aware adapter. A future Fanbase revision or
local grammar can supply that route after both controls and provenance pass.
