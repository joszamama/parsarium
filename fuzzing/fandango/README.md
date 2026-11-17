# Fandango specs

The [13-format default-route smoke](default-smoke-13.md) shows one fixed valid
generation, replay, and AFL++ preparation for each active format and pilot.

[Fandango](https://fandango-fuzzer.github.io/) 1.3.1 specs for six formats. MP4 and PDF use constraints to keep box sizes and offsets correct; the three text grammars keep headers and data consistent through their productions. Untagged MP3 targets spec reuses whole decoded frames from pinned controls.

```sh
python3 parsarium.py fandango setup
python3 parsarium.py fandango generate ascii_ply c assetkit runs/ply-fandango --count 100 --seed 1 --replay
```

The generator selects the bundled spec automatically, saves its hash and generated files, and can prepare the same corpus for AFL++ with `--prepare-afl`. [The MP4 and PDF grammar details](specs/README.md) describe their scope.

JSON and XML pilot targets default to Fanbase's `-F json` and `-F xml` specs. One fixed output from each was checked with Python's JSON or XML parser. Untagged MP3 targets (format directory `mp3`) default to a [small local grammar](specs/mp3_plain.fan) over six decodable, untagged Layer III streams. Fanbase's `-F mp3` output includes ID3 tags **and** Layer I/II frames; [stripping the tags is insufficient](plain-mp3-decision.md).

```sh
python3 parsarium.py fandango generate mp3 go github_com_dmulholl_mp3lib runs/mp3lib-fandango \
  --count 6 --seed 7 --replay --prepare-afl
python3 parsarium.py afl run runs/mp3lib-fandango/afl --check
```

The MP3 receipt names the local spec and hashes every generated file. Its
`format_validation` fields check contiguous Layer III frame headers and bind
the bundled outputs to six SHA-pinned samples decoded by the Go and Rust
adapters. A custom `--spec` gets the structural check without that decode
claim. The bundled grammar reuses pinned frame bytes and has limited variety.

```sh
python3 parsarium.py fandango generate json python simplejson runs/json-fandango \
  --count 10 --seed 42 --replay --prepare-afl
python3 parsarium.py fandango generate xml python xmltodict runs/xml-fandango \
  --count 10 --seed 42 --replay --prepare-afl
```

`parsarium.py report` can summarize the replayed inputs and outcomes. A replay does not measure source coverage; line views come from the parser's separate valid-control coverage directory after `parsarium.py build`.

| Spec | Cell | Scope |
| --- | --- | --- |
| [`mp4.fan`](specs/mp4.fan) | `mp4` | ISO BMFF with one 2×2 H.264 video frame, constrained box sizes and chunk offset; see [details](specs/README.md) |
| [`pdf.fan`](specs/pdf.fan) | `pdf` | One-page PDF with constrained xref offsets and stream length; see [details](specs/README.md) |
| [`ascii_ply.fan`](specs/ascii_ply.fan) | `ascii_ply` | `format ascii 1.0`; 3 vertices with 1 triangle or 4 vertices with 2 triangles; `float x y z`, optionally `uchar red green blue`; face list `uchar int` or `uchar uint`; 0–2 comment lines |
| [`ascii_pnm_p3.fan`](specs/ascii_pnm_p3.fan) | `ascii_pnm` | Plain PPM (`P3`) only; 1×1, 2×1, 1×2 or 2×2; maxval 255 or 15 with every sample at most maxval; space or newline header separators; optional comment after the magic; optional trailing newline |
| [`http11_request.fan`](specs/http11_request.fan) | `http11` | Requests only; `GET`, `HEAD`, `OPTIONS`, `DELETE` without body, or `POST` with a matching `Content-Length` (0, 3 or 9 bytes); origin-form targets; `Host` always present; optional `User-Agent`, `Accept`, `X-Parsarium`, `Connection`, each at most once; optional whitespace after the colon; CRLF line endings |
| [`mp3_plain.fan`](specs/mp3_plain.fan) | `mp3` untagged targets | Six whole-frame prefixes from two pinned, untagged Layer III controls; no ID3 tags or mixed layers |

Fanbase `ppm` covers both P3 and P6, so the PNM spec is restricted to P3. The `P1` and `P2` controls and HTTP responses are out of scope.

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
  -n 2 --random-seed 1 --progress-bar off -d /tmp/fandango/ascii_ply -x .ply
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

Fandango 1.3.1 parsed both seeded examples for each spec. Regenerating them with the same seed and `PYTHONHASHSEED=0` reproduced all six file hashes. Direct parser replays accepted 18 valid PLY examples with AssetKit, 18 P3 examples with PyQt5's `QImageReader`, and 34 HTTP/1.1 requests with libmicrohttpd. The two-example Parsarium replay commands above each returned `2 unique inputs, {'ok': 2}`. The HTTP sample included all five methods, and the PLY sample included both index types, both mesh sizes, and optional vertex colors.

AssetKit expands face corners in its mesh result, so a PLY header with four vertices and two triangles can report six output vertices. PyQt5 scales P3 samples declared with maxval 15 to 8-bit color values.

## Limits

The specs follow the PLY 1.0, Netpbm and RFC 9112 definitions. The validation covers one representative parser family per format; acceptance by every catalogued parser is not established. Variations that may separate parsers include the P3 comment line, maxval 15, newline-separated header fields, a missing trailing newline, `uint` face indices, `OPTIONS`/`DELETE`, and headers without a space after the colon.
