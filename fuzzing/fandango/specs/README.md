# Fandango specs

Small format-aware [Fandango](https://fandango-fuzzer.github.io/) 1.3.1 grammars that generate valid seed files.

`mp3_plain.fan` is a bounded pilot seed grammar. It embeds whole frames from
two pinned untagged controls and emits six decodable Layer III stream lengths.
It does not use Fanbase's mixed-layer, ID3-tagged `mp3` grammar.

| Spec | Structure | Varies | Checked with |
|---|---|---|---|
| `mp4.fan` | `ftyp`, `moov` (`mvhd`; an H.264 video `trak` with an `avc1` sample entry and one sample, an AAC audio `trak` with an `mp4a` sample entry and nine samples in one chunk, or both; optional `udta`/`meta`/`ilst`), one `mdat`, optional `free` boxes | video only, audio only, or video and audio; `mdat` before or after `moov`, and the video sample before or after the audio chunk; optional iTunes metadata with one to five of `©nam`, `©ART`, `©alb`, `©day` and `trkn`, holding 1–3 short ASCII words with at most one two- or three-byte UTF-8 character each, a year or full date, and a track number with or without a total; optional access unit delimiter in the sample, optional `pasp` and `btrt`, compressor name, brands and compatible-brand count, timescale, video duration, creation times, width/height, language and handler name per track, `free` payload | 200 outputs from `--random-seed 1 --max-nodes 2000`: ffprobe lists the expected streams and FFmpeg decodes all 200; `mp4/c/gpac` and `mp4/c/bento4` accept all 200 with the expected track counts; `mp4/cpp/opencv` and `mp4/cpp/exiv2` accept the 109 files with video and reject the 91 audio-only files, because both harnesses report video properties |
| `pdf.fan` | one page, five objects, classic `xref` table, trailer | PDF version, MediaBox, base font, 1–4 content-stream operators, text, title | `pdf/cpp/poppler`, `pdf/c/poppler-glib`, `pdf/cpp/podofo`, `qpdf --check` |
| `mp3_plain.fan` | untagged MPEG-1 or MPEG-2 Layer III stream | mono or stereo source, and 4, 8, or all source frames | `mp3/go/github_com_hajimehoshi_go_mp3`, `mp3/rust/symphonia_bundle_mp3` |
| `toml.fan` | TOML 1.0.0 document: root keys, optional `[server]`, `[owner]` and `[keys]` tables, zero to three `[[products]]` | `=` spacing, every integer base, float forms, basic and literal strings with escapes, arrays, inline tables, offset and local date-times | Python `tomllib` (200 of 200 outputs from `--random-seed 1`) |
| `dns_message.fan` | one DNS message (RFC 1035 section 4): a query with one question, or a response with one question and 1–4 answers | message ID, RD/RA/AA flags, question name and type, answer types (A, AAAA, CNAME, MX, TXT), TTLs, addresses, owner and target names written in full or as the pointer `C0 0C` | `controls/dns/check_controls.py` decoder |

Box sizes, the MP4 video sample size, both `stco` chunk offsets, the track and movie durations, xref offsets, the stream `/Length` and `startxref` are `where` constraints of the form `<field> == f(...)`, which Fandango repairs directly during generation.

```sh
fandango fuzz -f fuzzing/fandango/specs/mp4.fan -n 200 --random-seed 1 --max-nodes 2000 -d OUT -x .mp4
fandango parse -f fuzzing/fandango/specs/mp4.fan --file-mode binary OUT/*.mp4
```

Without `--max-nodes`, Fandango's default node budget keeps MP4 output at its smallest derivation: audio only, no metadata, one compatible brand and no `free`, `pasp`, `btrt` or access unit delimiter. `parsarium fandango generate` passes `--max-nodes 2000` with the bundled `mp4.fan`.

The MP4 SPS/PPS and IDR slice are copied byte for byte from the video track of `controls/mp4/red-av.mp4`, so every file decodes to the same 2×2 red frame. The coded size in `avc1` stays 2×2 to match the SPS. Only the `tkhd` display size varies.

The AAC sample entry (`mp4a` with `esds` and an optional `btrt`), the audio `stts`, `stsz` and the nine audio samples are copied byte for byte from the audio track of the same control, so every audio track decodes to one second of 8 kHz mono silence. The audio media timescale stays 8000; its `tkhd` duration is the 9024-sample media duration in the movie timescale, rounded up, and `mvhd` takes the longer of the two track durations. Track IDs are fixed (video 1, audio 2, next 3), so audio-only files have no track 1. The metadata follows the control's `udta` layout: `meta` with an `mdir` handler, then `ilst` items with one `data` box each.

Limitations: each MP4 has at most one video and one audio track. Their sample payloads are fixed: one 2×2 IDR frame and nine silent AAC frames, each track in a single chunk, with no edit lists, fragments or sample groups. Metadata items appear in a fixed order, at most once each, and only as UTF-8 text or `trkn`; no cover art, genre or freeform `----` items. With `--random-seed 1 --max-nodes 2000`, the 200 outputs split 52 video only, 91 audio only and 57 video and audio; 147 carry metadata. Object order and count in the PDF are fixed, because each offset constraint names the objects before it.
