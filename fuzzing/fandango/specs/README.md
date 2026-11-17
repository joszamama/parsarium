# Fandango specs

Small format-aware [Fandango](https://fandango-fuzzer.github.io/) 1.3.1 grammars that generate valid seed files.

| Spec | Structure | Varies | Checked with |
|---|---|---|---|
| `mp4.fan` | `ftyp`, `moov` (`mvhd`, one video `trak` with empty sample tables), optional `free` boxes | brands and compatible-brand count, timescale, duration, creation times, width/height, language, handler name, `free` payload | `mp4/c/bento4`, `mp4/cpp/exiv2` |
| `pdf.fan` | one page, five objects, classic `xref` table, trailer | PDF version, MediaBox, base font, 1–4 content-stream operators, text, title | `pdf/cpp/poppler`, `pdf/c/poppler-glib`, `pdf/cpp/podofo`, `qpdf --check` |

Box sizes, xref offsets, the stream `/Length` and `startxref` are `where` constraints of the form `<field> == f(...)`, which Fandango repairs directly. `fandango parse` rejects files whose sizes or offsets don't match.

```sh
fandango fuzz -f fuzzing/fandango/specs/mp4.fan -n 30 --random-seed 1 --max-nodes 2000 -d OUT -x .mp4
fandango parse -f fuzzing/fandango/specs/mp4.fan --file-mode binary OUT/*.mp4
```

Without `--max-nodes`, Fandango's default node budget keeps MP4 repetitions at their minimum: one compatible brand and no `free` box. Field values still vary.

Limitations: the MP4 track has no samples, so `mp4/cpp/opencv` (FFmpeg) rejects it with `invalid STSD entries 0`. Object order and count in the PDF are fixed, because each offset constraint names the objects before it.
