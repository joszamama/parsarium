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

The default `parsarium fandango generate mp3 ...` route therefore uses the
[local `mp3_plain.fan` grammar](specs/mp3_plain.fan), not `-F mp3`.

## 20 November 2026: generated audio

The first `mp3_plain.fan`, described in the rest of this note, chose among six
literal byte strings, so its language had exactly six words. Fandango keeps
only distinct outputs, and a 50-file request with seed 2027 returned six
files. The spec now generates the audio instead: 5 to 60 silent MPEG-1 or
MPEG-2 Layer III frames with one sample rate (32, 44.1 or 48 kHz; 16, 22.05 or
24 kHz), channel mode and CRC setting per file, a constant or per-frame
bitrate, and an optional Xing or Info frame. Frame lengths, CRCs and the Xing
counts are constraints over the headers. The same audio grammar is used by
[`mp3_tagged.fan`](specs/mp3_tagged.fan), which replaces Fanbase's `mp3` as
the tagged default. The checks and distributions are in
[the spec details](specs/README.md). The receipt keeps the structural check of
contiguous Layer III headers; the six-sample decode pin no longer applies.

## The first grammar (17 November 2026)

The first local grammar embeds
whole frames from two hash-pinned, untagged controls and selects one of three
complete frame-boundary prefixes from each. This yields six structurally
valid, tag-free Layer III streams. It is a bounded valid-frame seed generator:
it does not vary frame payloads or claim complete MP3 grammar coverage. The
source controls are `controls/mp3/go-tone-44k-mono.mp3` (SHA-256
`494492685c8ac5bfdbcbefa217c18a0fd4d2a44e21831e15a3fe0b0861d96c36`)
and `controls/mp3/go-tone-22k-stereo.mp3` (SHA-256
`e14721b65abfed142af10f51b43f29993a22003091eaa29086d2e36d7157761a`).
All six fixed-seed outputs decoded through both the pinned Go `go-mp3` and
Rust Symphonia adapters, each with exit status zero. Go reported the sample
rates in the table; Rust reported the decoded frame counts. The generator checks
contiguous Layer III headers and requires a known SHA from those six decoded
samples before replay or AFL++ preparation. It records each output's SHA-256,
size, and frame count. A custom `--spec` receives only the structural check;
its audio payload is not claimed to be decoded. No tag stripping is performed.

With `--count 6 --seed 7`, local spec SHA-256
`c3e773f45880cd27c09decb51496aa151ae27eef0afe031ac37f5bf6db6d24e0`
emitted these six files. Each was parsed directly with the pinned Go v0.3.4
adapter and Rust Symphonia 0.6.1 `/work/replay` in image
`sha256:169ba8c2b8700b50210814ab9f0be1a2e5e19824e2f33bdbc9ff132f8f21848f`;
Go returned the indicated sample rate and Rust returned the indicated frame
count. The Go package is pinned in its `go.mod` and source lock.

| Output | Bytes | SHA-256 | Sample rate | Frames |
| --- | ---: | --- | ---: | ---: |
| `fandango-0000.mp3` | 1,671 | `3353cac7b815fa1c23cb75424016fa85f5c41d773e07ee96e719a2f619dfb100` | 44,100 | 8 |
| `fandango-0001.mp3` | 1,254 | `e14721b65abfed142af10f51b43f29993a22003091eaa29086d2e36d7157761a` | 22,050 | 12 |
| `fandango-0002.mp3` | 2,298 | `494492685c8ac5bfdbcbefa217c18a0fd4d2a44e21831e15a3fe0b0861d96c36` | 44,100 | 11 |
| `fandango-0003.mp3` | 835 | `e0abae008e0954e26c4d9b3f8de7468646bc18e4608a808aadddd8afeb891516` | 44,100 | 4 |
| `fandango-0004.mp3` | 418 | `6a42b1d910bfdf6f28f643836ee9392c13984a440d3d896b618a8e5b3e4b9849` | 22,050 | 4 |
| `fandango-0005.mp3` | 836 | `53e7b1d51482221008d18ff0510c9810dbc651a59a93cb8017408c293ff528a1` | 22,050 | 8 |
