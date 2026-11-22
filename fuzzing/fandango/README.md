# Fandango specs

The [13-format default-route smoke](default-smoke-13.md) shows one fixed valid
generation, replay, and AFL++ preparation for each active format and pilot.

[Fandango](https://fandango-fuzzer.github.io/) 1.3.1 specs for seven formats. MP4 and PDF use constraints to keep box sizes and offsets correct, and ASCII PLY to keep element counts and vertex indices correct; SVG keeps every reference inside the file by fixed ids; the PNM and HTTP grammars keep headers and data consistent through their productions. The two MP3 specs derive every frame length, CRC, Xing count and ID3 size from the headers with constraints, and the WAV spec every chunk size, pad byte and `fact` sample count.

```sh
python3 parsarium.py fandango setup
python3 parsarium.py fandango generate ascii_ply c assetkit runs/ply-fandango --count 100 --seed 1 --replay
```

The generator selects the bundled spec automatically, saves its hash and generated files, and can prepare the same corpus for AFL++ with `--prepare-afl`. [The MP4, PDF, SVG and ASCII PLY grammar details](specs/README.md) describe their scope.

SVG targets default to the local [`svg.fan`](specs/svg.fan). Fanbase's `-F svg` stays selectable with `--fanbase svg`, but most of its outputs have a zero or near-zero width, height or viewBox, `<use>` or `url(#…)` references to ids the file does not define, or invalid property values such as `opacity: #90C`, so parser rejections there mostly measure the corpus.

WAV targets default to the local [`wav.fan`](specs/wav.fan). Fanbase's `-F wav` stays selectable with `--fanbase wav`, but every one of its outputs is invalid: the data chunk holds 2 to 64 bytes regardless of `nBlockAlign`, so 27 of 50 files are not a whole number of sample frames; the PCM files carry a `fact` chunk whose sample count is a random 32-bit value; and its IEEE-float `fmt` chunk is 16 bytes without `cbSize`. Rejections there mostly measure the corpus.

JSON and XML pilot targets default to Fanbase's `-F json` and `-F xml` specs. One fixed output from each was checked with Python's JSON or XML parser. MP3 targets verified on the ID3v2-tagged control default to the local [`mp3_tagged.fan`](specs/mp3_tagged.fan); Fanbase's `-F mp3` stays selectable with `--fanbase mp3`, but it keeps the audio frames fixed, mixes Layer III with Layer I and II frames, varies only the tag text and emits no TIT2, so almost every target gives one answer across its outputs. MP3 targets verified on untagged frames default to the local [`mp3_plain.fan`](specs/mp3_plain.fan), the same Layer III audio grammar without tags. Fanbase's `-F mp3` output includes ID3 tags **and** Layer I/II frames; [stripping the tags is insufficient](plain-mp3-decision.md). Fanbase has no TOML spec, so the TOML pilot defaults to the local [`toml.fan`](specs/toml.fan); 200 outputs from `--random-seed 1` were distinct and all parsed with Python's `tomllib`.

```sh
python3 parsarium.py fandango generate mp3 go github_com_dmulholl_mp3lib runs/mp3lib-fandango \
  --count 6 --seed 7 --replay --prepare-afl
python3 parsarium.py afl run runs/mp3lib-fandango/afl --check
```

The MP3 receipt names the local spec and hashes every generated file. Its
`format_validation` fields check contiguous, complete MPEG-1/2 Layer III frame
headers with one MPEG version and sample rate, and, on the tagged route, an
ID3v2.3/2.4 header, an ID3v1 trailer or both. The decode and tag checks of the
bundled specs are in [the spec details](specs/README.md).

```sh
python3 parsarium.py fandango generate json python simplejson runs/json-fandango \
  --count 10 --seed 42 --replay --prepare-afl
python3 parsarium.py fandango generate xml python xmltodict runs/xml-fandango \
  --count 10 --seed 42 --replay --prepare-afl
```

`parsarium.py report` can summarize the replayed inputs and outcomes. A replay does not measure source coverage; line views come from the parser's separate valid-control coverage directory after `parsarium.py build`.

| Spec | Cell | Scope |
| --- | --- | --- |
| [`mp4.fan`](specs/mp4.fan) | `mp4` | ISO BMFF with a 2×2 H.264 video frame, a silent AAC audio track, or both, and optional iTunes metadata; constrained box sizes, durations and chunk offsets; see [details](specs/README.md) |
| [`pdf.fan`](specs/pdf.fan) | `pdf` | PDF with one to five pages, per-page or inherited MediaBox, optional `/Rotate` and optional Info fields; constrained xref rows, object counts, stream lengths and `startxref`; see [details](specs/README.md) |
| [`svg.fan`](specs/svg.fan) | `svg` | SVG 1.1 documents with a positive width and height (1–512, unitless or px) and an optional positive viewBox; rect, circle, ellipse, line, polyline, polygon and path (M/L/H/V/C/Q/A/Z, absolute and relative), groups with transforms, hex, `rgb()` and named colors, opacity in [0, 1], optional title and desc, an optional linear gradient and `<use>` whose ids are defined in the same file; see [details](specs/README.md) |
| [`ascii_ply.fan`](specs/ascii_ply.fan) | `ascii_ply` | `format ascii 1.0` meshes with 3–60 vertices and 1–60 triangles, quads, pentagons and hexagons, optionally followed by an `edge` element, and point clouds without faces; `float` or `double` x/y/z, optional `float` normals and `uchar` RGB or RGBA; `uchar`, `int` or `uint` list counts and indices; 0–3 `comment`/`obj_info` lines; constrained element counts and in-range, distinct indices; see [details](specs/README.md) |
| [`ascii_pnm_p3.fan`](specs/ascii_pnm_p3.fan) | `ascii_pnm` | Plain PPM (`P3`) only; width and height 1–32; maxval 1–65535 (one alternative in five above 255); exactly width × height × 3 samples, each at most maxval, on lines of at most 70 characters; blank, tab, LF or CRLF header separators with optional comments before the width, height and maxval; one whitespace character after the maxval; white space after the last sample; see [details](specs/README.md) |
| [`http11_request.fan`](specs/http11_request.fan) | `http11` | Requests only; `GET`, `HEAD`, `OPTIONS`, `DELETE` without body, or `POST` with a matching `Content-Length` (0, 3 or 9 bytes); origin-form targets; `Host` always present; optional `User-Agent`, `Accept`, `X-Parsarium`, `Connection`, each at most once; optional whitespace after the colon; CRLF line endings |
| [`mp3_tagged.fan`](specs/mp3_tagged.fan) | tagged `mp3` targets | ID3v2.3 or 2.4 (TIT2, TPE1, TALB, TYER/TDRC, TRCK, TCON, COMM, each optional and at most once; ISO-8859-1, UTF-16 with BOM, UTF-8 in 2.4; optional padding), an optional ID3v1/1.1 trailer, or ID3v1 only, around the `mp3_plain.fan` audio; see [details](specs/README.md) |
| [`mp3_plain.fan`](specs/mp3_plain.fan) | untagged `mp3` targets | 5–60 silent MPEG-1 or MPEG-2 Layer III frames with one sample rate (32/44.1/48 or 16/22.05/24 kHz), channel mode and CRC setting per file; CBR or VBR; optional Xing/Info frame; no tags or other layers; see [details](specs/README.md) |
| [`yaml.fan`](specs/yaml.fan) | `yaml` pilot | One block-mapping document with fixed optional keys, flow and block collections, quoted scalars with escapes, block scalars and one anchor/alias; plain scalars typed the same under YAML 1.1 and the 1.2 core schema. Fanbase has no YAML spec |
| [`toml.fan`](specs/toml.fan) | `toml` pilot | TOML 1.0.0 documents with fixed key names per position: root keys, optional `[server]`, `[owner]` and dotted-key tables, zero to three `[[products]]`; typed integers, floats, strings with escapes, booleans, arrays, inline tables and date-times |
| [`wav.fan`](specs/wav.fan) | `wav` | RIFF/WAVE with PCM 8/16/24/32-bit, IEEE float 32/64-bit, or `WAVE_FORMAT_EXTENSIBLE` 16/24-bit PCM and 32-bit float in 1, 2, 4 or 6 channels; nine sample rates; `nBlockAlign` and `nAvgBytesPerSec` consistent with the format; whole sample frames; `fact` for non-PCM; optional `LIST`/`INFO` and `JUNK` chunks with pad bytes after odd-length chunks; see [details](specs/README.md) |
| [`dns_message.fan`](specs/dns_message.fan) | `dns` pilot | One DNS message: a query, or a response with 1–4 A, AAAA, CNAME, MX or TXT answers; counts fixed per alternative, `RDLENGTH` constrained, compression only by pointer to the question name at offset 12; see [decision](dns-decision.md) |

Fanbase `ppm` covers both P3 and P6, so the PNM spec is restricted to P3. Every `ascii_pnm` path is verified on the P3 control `red-green.ppm` and reports RGB fields, so the `P1` and `P2` controls stay out of the grammar, as do HTTP responses.

## Generate

For direct grammar use outside Parsarium, install the tested Fandango release in a local environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install 'fandango-fuzzer==1.3.1'
FANDANGO=.venv/bin/fandango
```

From the repository root:

```sh
PYTHONHASHSEED=0 $FANDANGO fuzz -f fuzzing/fandango/specs/ascii_ply.fan \
  -n 2 --random-seed 1 --max-nodes 5000 --progress-bar off -d /tmp/fandango/ascii_ply -x .ply
PYTHONHASHSEED=0 $FANDANGO fuzz -f fuzzing/fandango/specs/ascii_pnm_p3.fan \
  -n 2 --random-seed 1 --progress-bar off -d /tmp/fandango/ascii_pnm_p3 -x .ppm
PYTHONHASHSEED=0 $FANDANGO fuzz -f fuzzing/fandango/specs/http11_request.fan \
  -n 2 --random-seed 1 --progress-bar off -d /tmp/fandango/http11_request -x .http
```

With the same seed and `PYTHONHASHSEED`, repeated runs produce identical files. To check that a file matches its spec:

```sh
$FANDANGO parse -f fuzzing/fandango/specs/ascii_ply.fan /tmp/fandango/ascii_ply/fandango-0000.ply -o /dev/null
$FANDANGO parse -f fuzzing/fandango/specs/ascii_pnm_p3.fan /tmp/fandango/ascii_pnm_p3/fandango-0000.ppm -o /dev/null
$FANDANGO parse --file-mode binary -f fuzzing/fandango/specs/http11_request.fan \
  /tmp/fandango/http11_request/fandango-0000.http -o /dev/null
```

HTTP files need `--file-mode binary` for `parse`; text mode reads CRLF as LF and the parse fails. Generated files contain CRLF either way.

Replay generated files through representative Parsarium harnesses:

```sh
python3 parsarium.py replay ascii_ply c assetkit /tmp/fandango/ascii_ply runs/fandango-ply-assetkit \
  --per-case --generator Fandango --generator-version 1.3.1 --spec fuzzing/fandango/specs/ascii_ply.fan
python3 parsarium.py replay ascii_pnm python pyqt5 /tmp/fandango/ascii_pnm_p3 runs/fandango-pnm-pyqt5 \
  --per-case --generator Fandango --generator-version 1.3.1 --spec fuzzing/fandango/specs/ascii_pnm_p3.fan
python3 parsarium.py replay http11 c libmicrohttpd /tmp/fandango/http11_request runs/fandango-http-libmicrohttpd \
  --per-case --generator Fandango --generator-version 1.3.1 --spec fuzzing/fandango/specs/http11_request.fan
```

## Validation

The checks in this paragraph predate the wider `ascii_ply.fan` and `ascii_pnm_p3.fan`; their current validation is in the [spec details](specs/README.md). Fandango 1.3.1 parsed both seeded examples for each spec. Regenerating them with the same seed and `PYTHONHASHSEED=0` reproduced all six file hashes. Direct parser replays accepted 18 valid PLY examples with AssetKit, 18 P3 examples with PyQt5's `QImageReader`, and 34 HTTP/1.1 requests with libmicrohttpd. The two-example Parsarium replay commands above each returned `2 unique inputs, {'ok': 2}`. The HTTP sample included all five methods.

AssetKit expands face corners in its mesh result, so a PLY mesh can report one output vertex per face corner rather than the declared vertex count. PyQt5 scales P3 samples declared with maxval 15 to 8-bit color values.

## Limits

The specs follow the PLY 1.0, Netpbm and RFC 9112 definitions. The validation covers one representative parser family per format; acceptance by every catalogued parser is not established. Variations that may separate parsers include the P3 comment line, maxval 15, newline-separated header fields, a missing trailing newline, `uint` face indices, `OPTIONS`/`DELETE`, and headers without a space after the colon.
