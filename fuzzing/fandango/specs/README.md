# Fandango specs

Small format-aware [Fandango](https://fandango-fuzzer.github.io/) 1.3.1 grammars that generate valid seed files.

`mp3_tagged.fan` and `mp3_plain.fan` share one Layer III audio grammar; the
tagged spec wraps it in ID3v2 and ID3v1 tags. Neither uses Fanbase's
mixed-layer `mp3` grammar.

| Spec | Structure | Varies | Checked with |
|---|---|---|---|
| `mp4.fan` | `ftyp`, `moov` (`mvhd`; an H.264 video `trak` with an `avc1` sample entry and one sample, an AAC audio `trak` with an `mp4a` sample entry and nine samples in one chunk, or both; optional `udta`/`meta`/`ilst`), one `mdat`, optional `free` boxes | video only, audio only, or video and audio; `mdat` before or after `moov`, and the video sample before or after the audio chunk; optional iTunes metadata with one to five of `©nam`, `©ART`, `©alb`, `©day` and `trkn`, holding 1–3 short ASCII words with at most one two- or three-byte UTF-8 character each, a year or full date, and a track number with or without a total; optional access unit delimiter in the sample, optional `pasp` and `btrt`, compressor name, brands and compatible-brand count, timescale, video duration, creation times, width/height, language and handler name per track, `free` payload | 200 outputs from `--random-seed 1 --max-nodes 2000`: ffprobe lists the expected streams and FFmpeg decodes all 200; `mp4/c/gpac` and `mp4/c/bento4` accept all 200 with the expected track counts; `mp4/cpp/opencv` and `mp4/cpp/exiv2` accept the 109 files with video and reject the 91 audio-only files, because both harnesses report video properties |
| `pdf.fan` | catalog, a Pages node with one to five pages, each page followed by its own content stream, an Info dictionary, classic `xref` table, trailer | PDF version; page count 1–5 with matching `/Kids` and `/Count`; a MediaBox on every page, so pages in one file can differ, or one MediaBox inherited from the Pages node; optional `/Rotate` 0, 90, 180 or 270 per page; base font per page; per-page text and 0–3 further content-stream operators; zero to four of `/Title`, `/Author`, `/Subject` and `/Producer` | 200 outputs from `--random-seed 1 --max-nodes 2000`: `fandango parse`, `qpdf --check` and `mutool info` accept all 200, and both tools report the generated page count; `pdf/cpp/poppler`, `pdf/c/poppler-glib` and `pdf/cpp/podofo` accept all 200 with the generated page count |
| `svg.fan` | SVG 1.1 root in the SVG namespace with a width and height, optional `<title>` and `<desc>`, optional `<defs>`, an anchor shape, then further shapes, groups and `<use>` elements | width and height 1–512, unitless or `px`; with or without a viewBox (origin −16 to 4, size 48–128) and `preserveAspectRatio`; rect (optional `rx`/`ry`), circle, ellipse, line, polyline, polygon and path with absolute and relative M/L/H/V/C/Q/A/Z; `g` with up to three of translate, scale, rotate, skewX, skewY and matrix, nested once; fill and stroke as attributes or a `style` attribute, with hex, `rgb()` (integers or percentages) and named colors, stroke width, caps, joins and dashes; opacity, fill-opacity and stroke-opacity in [0, 1]; an optional `linearGradient` `g1` with two or three stops, used through `url(#g1)`; an optional shape `s1` in `<defs>` drawn by `<use xlink:href="#s1">` | 200 outputs from `parsarium fandango generate svg c librsvg … --count 200 --seed 1`: `xmllint` parses all 200; `rsvg-convert` 2.63.4 and the resvg 0.50.0 CLI render all 200 to rasters with painted pixels; the `svg/c/librsvg` harness accepts all 200; every `xlink:href` and `url(#…)` names an id defined in the same file |
| `ascii_ply.fan` | `ply`, `format ascii 1.0`, 0–3 `comment`/`obj_info` lines, a vertex element, then a face element (mesh), a face and an `edge` element, or no face element or `element face 0` (point cloud) | 3–60 vertices; `float` or `double` x/y/z, optional `float` nx/ny/nz, optional `uchar` RGB or RGBA; 1–60 faces of 3–6 distinct, in-range vertex indices; list count type `uchar`, `int` or `uint` and index type `int`, `uint` or `uchar`; property name `vertex_indices` or `vertex_index`; 1–20 edges with `int vertex1`/`vertex2` | 200 outputs from `parsarium fandango generate ascii_ply c assetkit … --count 200 --seed 1`: `fandango parse` and the Python `plyfile` 1.1 reader accept all 200, with every element count matching its rows and every face and edge index distinct and below the vertex count; `ascii_ply/rust/ply_rs` accepts all 200 and reports the declared vertex and face counts; `ascii_ply/cpp/open_mesh` accepts 158 and rejects the 42 with a `uint` list count type |
| `mp3_tagged.fan` | an ID3v2.3 or ID3v2.4 tag, an ID3v1 trailer or both, around the `mp3_plain.fan` audio | ID3v2 version; one to seven distinct frames of TIT2, TPE1, TALB, TYER (2.3) or TDRC (2.4), TRCK, TCON and COMM; text in ISO-8859-1, UTF-16 with a little- or big-endian BOM, or UTF-8 (2.4), including JSON-escaped punctuation and Latin-1, Cyrillic, CJK and astral characters; optional zero padding; optional ID3v1 or ID3v1.1 trailer with fixed-width zero-padded fields, or ID3v1 only | 200 outputs from `--random-seed 1 --max-nodes 2000`: own header and tag walk, mutagen 1.47.0 and ffprobe/ffmpeg 7.1.5 in a pinned `python:3.13-slim` image; every frame header parses, ffprobe counts the generated audio frames, mutagen reads back every ID3v2 frame and the ID3v1 trailer |
| `mp3_plain.fan` | untagged MPEG-1 or MPEG-2 Layer III stream | MPEG version and sample rate (32, 44.1, 48 kHz; 16, 22.05, 24 kHz), channel mode (stereo, joint stereo with mode extension 0–3, dual channel, mono), original bit, CRC, CBR or VBR, padding per frame, 5–60 audio frames, optional Xing or Info frame | 200 outputs from `--random-seed 1 --max-nodes 2000`: the same checks; ffmpeg decodes every file without a message |
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

```sh
fandango fuzz -f fuzzing/fandango/specs/mp3_tagged.fan -n 200 --random-seed 1 --max-nodes 2000 -d OUT -x .mp3
fandango fuzz -f fuzzing/fandango/specs/mp3_plain.fan -n 200 --random-seed 1 --max-nodes 2000 -d OUT -x .mp3
```

`mp3_tagged.fan` replaces Fanbase's `mp3` spec as the default route for MP3
targets verified on the ID3v2-tagged control; `--fanbase mp3` still selects it.
Fanbase's grammar keeps its eleven audio frames fixed, mixes Layer III with a
Layer II and a Layer I frame (mpg123 warns of a "Frankenstein stream"), varies
only the tag text, can repeat TALB and never emits TIT2, so on 50 outputs
almost every target gave one answer. `mp3_plain.fan` used to choose among six
literal whole-frame prefixes of two pinned controls, so its language had six
words and Fandango could emit at most six distinct files; it now generates
the audio.

Audio. A file's first frame fixes the MPEG version, sample rate, channel mode,
mode extension, flags and protection bit; constraints copy them into every
later frame. A constant-bitrate file repeats the first frame's bitrate (only
padding varies); a variable-bitrate file draws a bitrate index per frame.
Side information and main data are zeros, so every granule has
`part2_3_length` 0 and decodes to silence; each frame body is exactly the
header's frame length (`144000 * kbps / rate` for MPEG-1, `72000 * kbps / rate`
for MPEG-2, plus padding). A protected frame carries the CRC-16 of header bytes
3–4 and the side information. An optional first Xing frame (no CRC, same mode
and sample rate, the first frame's bitrate raised until the fields fit) holds
`Info` for CBR or `Xing` for VBR, the frames and bytes flags, the audio frame
count and the byte count of all MPEG frames. Files with a Xing frame have no
CRC. No MPEG-2.5, free format, emphasis, Layer I or II, or non-zero audio.

Tags. ID3v2 has no unsynchronisation, extended header or footer; frame flags
are zero; 2.3 frame sizes are 32-bit and 2.4 sizes synchsafe; the tag size is
synchsafe and covers the frames and optional padding. Text has no terminator.
Frames appear in a fixed order and each at most once. TCON is `(N)` or a name
in 2.3 and `N` or a name in 2.4; TRCK is `N` or `N/M`; COMM has a language,
a short ASCII description and text, with a BOM before each UTF-16 string.
Three of the four top-level alternatives carry an ID3v2 tag; ID3v1 fields are
drawn independently of ID3v2, so a reader that prefers one tag can differ from
one that prefers the other.

With `--random-seed 1 --max-nodes 2000`, the 200 `mp3_tagged.fan` outputs
split 26 ID3v2.3, 41 ID3v2.3 + ID3v1, 51 ID3v2.4, 49 ID3v2.4 + ID3v1 and 33
ID3v1 only; MPEG-1 at 32/44.1/48 kHz in 34/21/36 files and MPEG-2 at
16/22.05/24 kHz in 22/50/37; stereo 22, joint 42, dual 51, mono 85; CRC in 65;
Info 57 and Xing 33; VBR 102; 5–60 audio frames (mean 26). Among the 167
ID3v2 tags, TIT2 is in 116, TPE1 100, TALB 85, TYER 33, TDRC 71, TRCK 84,
TCON 117 and COMM 97; 141 tags use ISO-8859-1, 158 UTF-16 and 86 UTF-8; 76
have padding. Files are 688 to 54,857 bytes. The 200 `mp3_plain.fan` outputs
split MPEG-1 at 32/44.1/48 kHz in 34/46/25 files and MPEG-2 at 16/22.05/24 kHz
in 39/34/22; stereo 54, joint 48, dual 48, mono 50; CRC in 48; Info 63 and
Xing 22; VBR 71; 5–60 audio frames (mean 33); 260 to 44,238 bytes. All 400
are distinct, and Fandango's output depends on the seed, so a 50-file corpus
can split differently.

```sh
fandango fuzz -f fuzzing/fandango/specs/svg.fan -n 200 --random-seed 1 --max-nodes 2000 -d OUT -x .svg
fandango parse -f fuzzing/fandango/specs/svg.fan OUT/*.svg
```

`svg.fan` replaces Fanbase's `svg` spec as the default SVG route. Fanbase's output is well-formed XML, but most files have a zero or near-zero width, height or viewBox (`width="0.03pt"`, `viewBox="0 -838 0 0.5"`), `<use>` and `url(#…)` references to ids the file does not define, or invalid property values (`opacity: #90C`, a color where a number belongs), so a parser that rejects them is usually right. `--fanbase svg` still selects it.

Every `svg.fan` document is one of four variants: no `<defs>`, a gradient `g1`, a reusable shape `s1`, or both. A variant defines only fixed ids and uses each at least once, and only a variant that defines an id may refer to it, so every reference resolves. `xmlns:xlink` is declared exactly when the file contains `<use>`. Without a viewBox the user space is the viewport, so width and height are at least 32; with one, the viewBox always contains the square from 4 to 32 user units. The first drawn element is an anchor (rect, circle, ellipse or closed path) with solid paint and opacity at least 0.6 that always overlaps that square, so every file renders to a non-empty raster. The anchor may start at (0, 0), so some files paint the top-left pixel and others do not. Without `--max-nodes`, Fandango's default node budget yields one to six shapes, groups or `<use>` elements per file; `parsarium fandango generate` passes `--max-nodes 2000` with the bundled `svg.fan`.

SVG limitations: no text, fonts, images, scripts, animation, CSS `<style>` sheets, DOCTYPE, external references, masks, clip paths, filters, patterns, markers or radial gradients; at most one gradient and one reusable shape per file; ids are fixed (`g1`, `s1`). Coordinates are small decimals (at most one fractional digit). With `parsarium fandango generate svg c librsvg … --count 200 --seed 1`, the 200 files split 44 without defs, 56 with a gradient only, 38 with `<use>` only and 62 with both (118 gradient, 100 `<use>`); 81 have a viewBox (31 of them a `preserveAspectRatio`) and 144 use `px`. Widths run 3–512 and heights 1–512; 17 files have a side of 16 or less. Files hold 1 to 20 drawn shapes (1,377 in all): rect in 147 files (272 elements), circle 123 (262), ellipse 136 (270), path 145 (217), polygon 74 (105), polyline 65 (80), line 69 (106), `use` 100 (165), and `g` in 135 files (408 groups). 182 files use a `style` attribute; 83 have a title and 136 a desc. `rsvg-convert` paints the top-left pixel in 45 files and resvg in 43. Files are 246 to 3,155 bytes.

```sh
fandango fuzz -f fuzzing/fandango/specs/ascii_ply.fan -n 200 --random-seed 1 --max-nodes 5000 -d OUT -x .ply
fandango parse -f fuzzing/fandango/specs/ascii_ply.fan OUT/*.ply
```

Each `ascii_ply.fan` alternative fixes the vertex layout and which elements follow, so the header declares exactly the properties and elements the body holds. Element counts are `where` constraints of the form `<count> == f(...)` over the generated rows. Face and edge rows are repaired the same way: the generated indices are taken modulo the vertex count and bumped until distinct, and a face with more corners than the mesh has vertices keeps only as many corners as there are vertices. Without `--max-nodes`, Fandango's default node budget yields only a few vertices and faces, with no normals or alpha; `parsarium fandango generate` passes `--max-nodes 5000` with the bundled `ascii_ply.fan`.

The grammar weights plain meshes, meshes with an edge element and point clouds 19:4:1. Point clouds have fewer constraints to repair, so Fandango's search keeps more of them than the weights alone give; the share varies by seed (16% for seed 1, 6% for 50 files at seed 2027).

ASCII PLY limitations: every file is ASCII, LF-terminated and uses single spaces; no binary formats, no type aliases such as `float32` or `uint8`, no per-face properties other than the index list, no other elements, and properties appear in a fixed order (x/y/z, normals, colour). Coordinates are decimals below 100 in magnitude with at most four fractional digits, and normals are components in [−1, 1], not necessarily unit length. Faces join random vertices, so meshes are rarely manifold: OpenMesh accepts such a file but splits vertices or drops faces it cannot add, so its counts often differ from the header. With `parsarium fandango generate ascii_ply c assetkit … --count 200 --seed 1`, the 200 files (198 distinct) hold 3–60 vertices (median 27): 168 meshes, 47 of them with 1–20 edges (456 in all), and 32 point clouds (22 without a face element, 10 with `element face 0`). Meshes have 1–60 faces (median 32; 5,119 in all: 2,104 triangles, 2,161 quads, 447 pentagons, 407 hexagons). Vertex layouts: 37 x/y/z only, 40 RGB, 39 RGBA, 30 normals, 34 normals and RGB, 20 normals and RGBA; 118 use `double` coordinates. List count types are `uchar` in 82 meshes, `int` in 44 and `uint` in 42; index types `int` in 66, `uint` in 61 and `uchar` in 41; 98 name the list `vertex_indices` and 70 `vertex_index`. 104 files have a comment and 122 an `obj_info` line. Files are 229 to 3,046 bytes.
