# Fandango specs

Small format-aware [Fandango](https://fandango-fuzzer.github.io/) 1.3.1 grammars that generate valid seed files.

`mp3_plain.fan` is a bounded pilot seed grammar. It embeds whole frames from
two pinned untagged controls and emits six decodable Layer III stream lengths.
It does not use Fanbase's mixed-layer, ID3-tagged `mp3` grammar.

| Spec | Structure | Varies | Checked with |
|---|---|---|---|
| `mp4.fan` | `ftyp`, `moov` (`mvhd`; an H.264 video `trak` with an `avc1` sample entry and one sample, an AAC audio `trak` with an `mp4a` sample entry and nine samples in one chunk, or both; optional `udta`/`meta`/`ilst`), one `mdat`, optional `free` boxes | video only, audio only, or video and audio; `mdat` before or after `moov`, and the video sample before or after the audio chunk; optional iTunes metadata with one to five of `©nam`, `©ART`, `©alb`, `©day` and `trkn`, holding 1–3 short ASCII words with at most one two- or three-byte UTF-8 character each, a year or full date, and a track number with or without a total; optional access unit delimiter in the sample, optional `pasp` and `btrt`, compressor name, brands and compatible-brand count, timescale, video duration, creation times, width/height, language and handler name per track, `free` payload | 200 outputs from `--random-seed 1 --max-nodes 2000`: ffprobe lists the expected streams and FFmpeg decodes all 200; `mp4/c/gpac` and `mp4/c/bento4` accept all 200 with the expected track counts; `mp4/cpp/opencv` and `mp4/cpp/exiv2` accept the 109 files with video and reject the 91 audio-only files, because both harnesses report video properties |
| `pdf.fan` | catalog, a Pages node with one to five pages, each page followed by its own content stream, an Info dictionary, classic `xref` table, trailer | PDF version; page count 1–5 with matching `/Kids` and `/Count`; a MediaBox on every page, so pages in one file can differ, or one MediaBox inherited from the Pages node; optional `/Rotate` 0, 90, 180 or 270 per page; base font per page; per-page text and 0–3 further content-stream operators; zero to four of `/Title`, `/Author`, `/Subject` and `/Producer` | 200 outputs from `--random-seed 1 --max-nodes 2000`: `fandango parse`, `qpdf --check` and `mutool info` accept all 200, and both tools report the generated page count; `pdf/cpp/poppler`, `pdf/c/poppler-glib` and `pdf/cpp/podofo` accept all 200 with the generated page count |
| `mp3_plain.fan` | untagged MPEG-1 or MPEG-2 Layer III stream | mono or stereo source, and 4, 8, or all source frames | `mp3/go/github_com_hajimehoshi_go_mp3`, `mp3/rust/symphonia_bundle_mp3` |
| `toml.fan` | TOML 1.0.0 document: root keys, optional `[server]`, `[owner]` and `[keys]` tables, zero to three `[[products]]` | `=` spacing, every integer base, float forms, basic and literal strings with escapes, arrays, inline tables, offset and local date-times | Python `tomllib` (200 of 200 outputs from `--random-seed 1`) |
| `dns_message.fan` | one DNS message (RFC 1035 section 4): a query with one question, or a response with one question and 1–4 answers | message ID, RD/RA/AA flags, question name and type, answer types (A, AAAA, CNAME, MX, TXT), TTLs, addresses, owner and target names written in full or as the pointer `C0 0C` | `controls/dns/check_controls.py` decoder |

Box sizes, the MP4 video sample size, both `stco` chunk offsets, the track and movie durations, the PDF xref rows, the xref and `/Size` object counts, every stream `/Length` and `startxref` are `where` constraints of the form `<field> == f(...)`, which Fandango repairs directly during generation.

```sh
fandango fuzz -f fuzzing/fandango/specs/mp4.fan -n 200 --random-seed 1 --max-nodes 2000 -d OUT -x .mp4
fandango parse -f fuzzing/fandango/specs/mp4.fan --file-mode binary OUT/*.mp4
```

Without `--max-nodes`, Fandango's default node budget keeps MP4 output at its smallest derivation: audio only, no metadata, one compatible brand and no `free`, `pasp`, `btrt` or access unit delimiter. `parsarium fandango generate` passes `--max-nodes 2000` with the bundled `mp4.fan`.

The MP4 SPS/PPS and IDR slice are copied byte for byte from the video track of `controls/mp4/red-av.mp4`, so every file decodes to the same 2×2 red frame. The coded size in `avc1` stays 2×2 to match the SPS. Only the `tkhd` display size varies.

The AAC sample entry (`mp4a` with `esds` and an optional `btrt`), the audio `stts`, `stsz` and the nine audio samples are copied byte for byte from the audio track of the same control, so every audio track decodes to one second of 8 kHz mono silence. The audio media timescale stays 8000; its `tkhd` duration is the 9024-sample media duration in the movie timescale, rounded up, and `mvhd` takes the longer of the two track durations. Track IDs are fixed (video 1, audio 2, next 3), so audio-only files have no track 1. The metadata follows the control's `udta` layout: `meta` with an `mdir` handler, then `ilst` items with one `data` box each.

```sh
fandango fuzz -f fuzzing/fandango/specs/pdf.fan -n 200 --random-seed 1 --max-nodes 2000 -d OUT -x .pdf
fandango parse -f fuzzing/fandango/specs/pdf.fan --file-mode binary OUT/*.pdf
```

Each page count is its own alternative with a literal `/Kids` array and `/Count`, and object numbers follow the position in the tree: catalog 1, Pages 2, Info 3, page k at 2k+2 and its content stream at 2k+3. The xref rows are one constraint over the body bytes: a helper finds each `N 0 obj` line and writes the offsets in object-number order, so no constraint names the objects before a given one. Without `--max-nodes`, Fandango's default node budget yields only one- or two-page files; `parsarium fandango generate` passes `--max-nodes 2000` with the bundled `pdf.fan`.

Limitations: each MP4 has at most one video and one audio track. Their sample payloads are fixed: one 2×2 IDR frame and nine silent AAC frames, each track in a single chunk, with no edit lists, fragments or sample groups. Metadata items appear in a fixed order, at most once each, and only as UTF-8 text or `trkn`; no cover art, genre or freeform `----` items. With `--random-seed 1 --max-nodes 2000`, the 200 outputs split 52 video only, 91 audio only and 57 video and audio; 147 carry metadata.

PDF limitations: one flat Pages node, a standard Type1 font per page, uncompressed content streams and a single classic xref table; no outlines, annotations, images, object streams, cross-reference streams or incremental updates. The Info object is always present, possibly empty, and its fields appear in a fixed order. With `--random-seed 1 --max-nodes 2000`, the 200 outputs have one to five pages in 25, 22, 31, 49 and 73 files (723 pages); 107 files give each page its own MediaBox, 93 of them with differing boxes across pages, and 93 inherit one MediaBox from the Pages node. 182 files set `/Rotate` on at least one page (430 pages: 108 at 0, 127 at 90, 77 at 180, 118 at 270). The Info dictionary is empty in 79 files and holds `/Title` in 53, `/Author` in 54, `/Subject` in 51 and `/Producer` in 73. Files are 631 to 2,327 bytes.
