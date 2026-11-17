# Fandango specs

Small format-aware [Fandango](https://fandango-fuzzer.github.io/) 1.3.1 grammars that generate valid seed files.

`mp3_plain.fan` is a bounded pilot seed grammar. It embeds whole frames from
two pinned untagged controls and emits six decodable Layer III stream lengths.
It does not use Fanbase's mixed-layer, ID3-tagged `mp3` grammar.

| Spec | Structure | Varies | Checked with |
|---|---|---|---|
| `mp4.fan` | `ftyp`, `moov` (`mvhd`, one H.264 video `trak` with an `avc1` sample entry and one sample), `mdat` with one 2×2 IDR frame, optional `free` boxes | `mdat` before or after `moov`, optional access unit delimiter in the sample, optional `pasp`, compressor name, brands and compatible-brand count, timescale, duration, creation times, width/height, language, handler name, `free` payload | `mp4/c/gpac`, `mp4/cpp/opencv`, `mp4/c/bento4`, `mp4/cpp/exiv2` |
| `pdf.fan` | one page, five objects, classic `xref` table, trailer | PDF version, MediaBox, base font, 1–4 content-stream operators, text, title | `pdf/cpp/poppler`, `pdf/c/poppler-glib`, `pdf/cpp/podofo`, `qpdf --check` |
| `mp3_plain.fan` | untagged MPEG-1 or MPEG-2 Layer III stream | mono or stereo source, and 4, 8, or all source frames | `mp3/go/github_com_hajimehoshi_go_mp3`, `mp3/rust/symphonia_bundle_mp3` |
| `toml.fan` | TOML 1.0.0 document: root keys, optional `[server]`, `[owner]` and `[keys]` tables, zero to three `[[products]]` | `=` spacing, every integer base, float forms, basic and literal strings with escapes, arrays, inline tables, offset and local date-times | Python `tomllib` (200 of 200 outputs from `--random-seed 1`) |
| `dns_message.fan` | one DNS message (RFC 1035 section 4): a query with one question, or a response with one question and 1–4 answers | message ID, RD/RA/AA flags, question name and type, answer types (A, AAAA, CNAME, MX, TXT), TTLs, addresses, owner and target names written in full or as the pointer `C0 0C` | `controls/dns/check_controls.py` decoder |

Box sizes, the MP4 sample size and `stco` chunk offset, xref offsets, the stream `/Length` and `startxref` are `where` constraints of the form `<field> == f(...)`, which Fandango repairs directly during generation.

```sh
fandango fuzz -f fuzzing/fandango/specs/mp4.fan -n 30 --random-seed 1 --max-nodes 2000 -d OUT -x .mp4
fandango parse -f fuzzing/fandango/specs/mp4.fan --file-mode binary OUT/*.mp4
```

Without `--max-nodes`, Fandango's default node budget keeps MP4 repetitions at their minimum: one compatible brand and no `free`, `pasp` or access unit delimiter. Field values and `mdat` placement still vary.

The MP4 SPS/PPS and IDR slice are copied byte for byte from the video track of `controls/mp4/red-av.mp4`, so every file decodes to the same 2×2 red frame. The coded size in `avc1` stays 2×2 to match the SPS. Only the `tkhd` display size varies.

Limitations: the MP4 has one video track with one sample and no audio. Object order and count in the PDF are fixed, because each offset constraint names the objects before it.
