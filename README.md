# Parsarium

Parsarium is a reproducible catalogue of libraries and bundled APIs that parse
specific formats. It currently contains a verified JavaScript × PNG pilot,
JavaScript × ZIP, MP4, WAV, PDF, SVG, HTTP/1.1, and MP3 with ID3v2 batches,
Go × ZIP, PNG, WAV, HTTP/1.1, MP4, MP3 with ID3v2, PDF, SVG, and ASCII PNM,
Python × PNG, ASCII PNM, ZIP, WAV, and PDF, and an explicit 88-cell work matrix. The other 66 cells
are marked `not_started`;
a zero in those cells does **not** mean no parser exists. See the
[selection protocol](PROTOCOL.md) before adding a package.

## Reproduce the verified cells

The recorded run used macOS arm64, Python 3.14.7, Node.js 26.10.0, npm 11.19.1,
and Chromium 153.0.8010.12 through Playwright 1.63.0. The npm lockfile pins
all packages and integrity hashes. From the repository root:

```sh
npm ci
npx playwright install chromium
npm run pilot:control
npm run pilot:verify
npm run zip:control
npm run zip:verify
npm run mp4:control
npm run mp4:verify
npm run mp3_id3v2:control
npm run mp3_id3v2:verify
npm run wav:control
npm run wav:verify
npm run pdf:control
npm run pdf:verify
npm run svg:control
npm run svg:verify
npm run http11:control
npm run http11:verify
python3 scripts/verify_go_zip.py
python3 scripts/verify_go_png.py
python3 scripts/verify_go_wav.py
python3 scripts/verify_go_http11.py
python3 scripts/verify_go_mp4.py
python3 scripts/verify_go_mp3_id3v2.py
python3 scripts/verify_go_pdf.py
python3 scripts/verify_go_svg.py
python3 controls/ascii_pnm/make_control.py
python3 scripts/verify_go_ascii_pnm.py
uv venv --python python3.13 adapters/python/png/.venv
uv pip sync adapters/python/png/requirements.lock --python adapters/python/png/.venv/bin/python --require-hashes
python3 scripts/verify_python_png.py
uv venv --python python3.13 adapters/python/ascii_pnm/.venv
uv pip sync adapters/python/ascii_pnm/requirements.lock --python adapters/python/ascii_pnm/.venv/bin/python --require-hashes
python3 scripts/verify_python_ascii_pnm.py
uv venv --python python3.13 adapters/python/zip/.venv
uv pip sync adapters/python/zip/requirements.lock --python adapters/python/zip/.venv/bin/python --require-hashes
adapters/python/zip/.venv/bin/python controls/zip/make_zstd_control.py
python3 controls/zip/make_module_control.py
python3 scripts/verify_python_zip.py
uv venv --python python3.13 adapters/python/wav/.venv
uv pip sync adapters/python/wav/requirements.lock --python adapters/python/wav/.venv/bin/python --require-hashes
python3 scripts/verify_python_wav.py
uv venv --python python3.13 adapters/python/pdf/.venv
uv pip sync adapters/python/pdf/requirements.lock --python adapters/python/pdf/.venv/bin/python --require-hashes
uv venv --python python3.13 adapters/python/pdf/.venv_pdfx
uv pip sync adapters/python/pdf/requirements-pdfx.lock --python adapters/python/pdf/.venv_pdfx/bin/python --require-hashes
uv venv --python python3.13 adapters/python/pdf/.venv_slate
uv pip sync adapters/python/pdf/requirements-slate3k.lock --python adapters/python/pdf/.venv_slate/bin/python --require-hashes
python3 scripts/verify_python_pdf.py
python3 scripts/build_matrix.py
python3 scripts/build_rankings.py
python3 scripts/validate_catalog.py
```

`pilot:control` generates the 71-byte PNG in `controls/png/red-green.png` with
SHA-256 `5a852fbaaaecaf4cd14c01e150c7f881c5c5894b0a1e3c53be7e007c58374ee6`.
It has two opaque pixels: red and green. The verifier runs each package adapter
against the path, checks parsed dimensions and either decoded pixels, parsed
chunks, or the format-bearing header result, then writes dated JSON results.
It also runs the browser-bundled `createImageBitmap(Blob)` adapter with the same
control. The observed pilot result is **21/21 third-party packages and 1/1
runtime API passing**. A fresh run replaces the dated result files.
It also generates `controls/png/red-green-title.png`, the same valid pixels
with a `Title=Parsarium` text chunk for metadata readers.

`zip:control` creates a deterministic 128-byte ZIP with one DEFLATE-compressed
`hello.txt` entry containing `parsarium\n` (SHA-256
`c534fa083d1da92474852ca9168ba0793740c25205f828915a1d862bd78c776b`).
The ZIP adapter checks both the parsed entry name and decompressed content.
The observed batch result is **21/21 third-party packages and 1/1 Node.js
built-in API passing**.

`mp4:control` restores a fixed 2670-byte MP4 with one 2×2 H.264 video frame,
one second of silent 8 kHz AAC audio, title `Parsarium`, and creation time
`2020-01-02T03:04:05Z` (SHA-256
`10086c39c7226726579924794cd7c0bbafe65de38021bd0f38f6da9d23d24643`).
The source bytes are committed as base64, so FFmpeg is not needed to reproduce
the control. Package adapters check parsed boxes, tracks, audio samples, title,
or creation time according to their documented scope. The observed result is
**20/20 third-party packages and 1/1 browser runtime API passing**. Some
packages parse only a header or metadata field; `mp4-metadata` needs a
`FileReader` compatibility adapter in Node. The ranking labels each scope.

`mp3_id3v2:control` restores a fixed 4997-byte MP3 with one second of 440 Hz
mono audio at 8000 Hz and ID3v2.3 title `Parsarium`, artist `Control`, and
album `Pilot` (SHA-256
`d61e1802a52dc55b5447356a3347fa4f9e08eb706757870f65ee0776dbf5bcad`).
The committed base64 source removes the need for FFmpeg during verification.
Adapters check parsed tags, audio samples, or duration according to each
package's documented scope. The observed result is **24/24 third-party
packages and 2/2 browser runtime APIs passing**. Duration readers disagree
because they account for encoder padding differently; the verification file
records each observed value. The browser APIs decode audio or read duration but
do not expose ID3v2 fields.

`wav:control` creates a deterministic 52-byte mono PCM RIFF/WAVE file with four
16-bit samples at 8000 Hz (SHA-256
`6154e1a5105d7b8b35a7ac228d50907c2fed58ea63577391b34957cc538966ce`).
The WAV adapter checks parsed sample rate, channel count, and either PCM sample
signs, bit depth, or the exact 0.0005-second duration, according to each
documented API's scope. The observed batch result is **22/22 third-party
packages and 1/1 browser-bundled API passing**. Header-only and duration-only
readers are labeled in the ranking. Three header-reader packages report a
duration inconsistent with the control's four samples, so their duration is
not used as verification evidence.

`pdf:control` creates a deterministic 696-byte PDF 1.4 file with one letter-size
page, the title `Parsarium PDF control`, and searchable text `Parsarium`
(SHA-256 `9bbfad1ba7ac5d0f4e25dd1d2e00c9f4cc7a493e303034b5884759f42ec5f60a`).
The PDF adapter checks extracted text or documented page/title fields. The
observed batch result is **22/22 third-party packages passing**. No PDF parser
was found in the scoped Node.js core or browser JavaScript API documentation;
the separate runtime record states those search limits. Browser PDF display
alone does not expose a parsed PDF result to JavaScript.

`http11:control` creates deterministic, valid HTTP/1.1 request and response
wire files. The request is a GET for `/parsarium?x=1` with a Host field; the
response is `200 OK` with the nine-byte body `parsarium` and a matching
Content-Length. The adapter checks parsed method and target or status and body.
The observed batch result is **20/20 third-party packages and 1/1 Node.js
runtime API passing**. Several packages are forks or distributions of the
same underlying parser; the family column records this relationship. The
simple controls establish only these specific parsing paths.

`svg:control` creates a deterministic 196-byte SVG with a red and a green
rectangle in a 2×1 viewport. The adapters check element structure, dimensions,
colors, converted paths, or exact rendered pixels according to each package's
documented scope. The observed batch result is **22/22 third-party packages
passing**. The separate browser run verifies both `DOMParser` with typed SVG
elements and `HTMLImageElement` decoding from a local SVG Blob. A direct
`createImageBitmap(Blob)` attempt failed on the control in this Chromium build;
it is recorded as a candidate failure, not a verified API.

`verify_go_zip.py` uses Go 1.27.1 and the shared deterministic ZIP control.
The Go module at `adapters/go/zip` pins third-party releases in `go.mod` and
checksums in `go.sum`. The adapters check the parsed entry name and
decompressed text. The observed result is **23/23 third-party packages and
1/1 Go standard-library API passing**. Several packages wrap or fork
`archive/zip`; the ranking records their parser families.

`verify_go_png.py` uses Go 1.27.1 and the shared two-pixel PNG control.
`adapters/go/png/go.mod` and `go.sum` pin all Go modules. The bimg and govips
adapters require libvips, and the imagick adapter requires ImageMagick
MagickWand, with their development headers and `pkg-config` files. The
recorded run used libvips 8.18.7 and ImageMagick 7.1.2. Check the local
installation with `pkg-config --modversion vips` and
`pkg-config --modversion MagickWand`. The observed result is **20/20
third-party packages and 3/3 Go standard-library API paths passing**.
Pixel readers, chunk readers, converters, and dimension readers have distinct
scopes in the ranking; several packages share Go's `image/png` decoder or
libvips.

`verify_go_wav.py` uses Go 1.27.1 and the shared four-sample PCM16 WAV control.
`adapters/go/wav/go.mod` and `go.sum` pin the releases. The observed result is
**21/21 third-party packages passing**. The separate Go 1.27.1 standard-library
inventory documents no WAV-aware parser API; generic file and binary readers
do not qualify. The `cryptix/wav` adapter verifies its parsed header and sample
count, since a sample value disagreed with the control's signed PCM.

`verify_go_http11.py` uses Go 1.27.1 and the shared valid request and response
wire controls. `adapters/go/http11/go.mod` and `go.sum` pin the releases. The
observed result is **20/20 third-party packages and 2/2 Go standard-library
API paths passing**. Request-line and request-header-only readers are labeled
by scope. Several packages share `net/http` or `fasthttp` parser lineages;
the package count does not imply 20 independent parser engines.

`verify_go_mp4.py` uses Go 1.27.1 and the shared progressive MP4 control.
`adapters/go/mp4/go.mod` and `go.sum` pin the releases. The observed result is
**20/20 third-party packages passing**. The adapters report parsed movie-box
size, MP4 brand, track or stream count, or title according to the documented
API. The ranking labels narrow `ftyp` and metadata scopes and shared parser
families. The separate standard-library inventory records no MP4-aware API
in the scoped Go 1.27.1 docs.

`verify_go_mp3_id3v2.py` uses Go 1.27.1 and the committed 44.1 kHz MPEG-1
Layer III control with ID3v2.3 title `Parsarium`. Its source bytes are restored
by `python3 controls/mp3_id3v2/make_control.py`, alongside the earlier 8 kHz
control. The observed result is **20/20 third-party packages passing**. Audio
decoders, MPEG frame readers, duration readers, and ID3v2 title readers have
separate scopes in the ranking. Two duration readers include encoder padding in
their reported 1071 ms; one tag reader preserves a trailing NUL in the title.
The Go 1.27.1 standard-library inventory records no MP3 or ID3v2 parser API.

`verify_go_pdf.py` uses Go 1.27.3 and the shared valid one-page PDF control.
`adapters/go/pdf/go.mod` and `go.sum` pin its releases. The observed result is
**20/20 third-party packages passing**. Adapters report page count, extracted
text, PDF version, or parsed indirect-object count according to their documented
scope. Many packages share the rsc PDF reader lineage; the ranking records this.
The separate Go 1.27.3 standard-library inventory documents no PDF document
parser API. The go-fitz adapter uses MuPDF code bundled by its Go module.

`verify_go_svg.py` uses Go 1.27.1 and the shared two-rectangle SVG control.
`adapters/go/svg/go.mod` and `go.sum` pin its releases. The observed result is
**21/21 third-party packages passing**. Adapters report parsed shapes, paths,
viewBox size, rendered pixels, or SVG-aware minified markup according to their
documented scope. Several readers share `oksvg` or Goki/Cogent code lineages.
The separate Go 1.27.1 standard-library inventory finds no SVG-aware parser;
generic XML parsing is outside the cell's parser criterion.

`verify_go_ascii_pnm.py` uses Go 1.27.1 and a valid 2×1 ASCII P3 PPM control
with red and green pixels (SHA-256
`f1e86f7bc611601fed6f44a263d8c1f026dd1d0fd66a7dbc8530e245f5561bf1`).
`make_control.py` also creates valid P1 PBM and P2 PGM files for future
variant-specific checks. The observed result is **20/20 third-party packages
passing on P3**. The ranking labels a header-only reader and dimension-only
native bindings; it does not claim that every package handles all PNM variants.
Five accepted bindings use libvips 8.18.7, and one uses ImageMagick 7.1.2.
Install their development headers and `pkg-config` files before rerunning.
`adapters/go/ascii_pnm/go.mod` and `go.sum` pin dependencies. `go mod verify`
passes; plain `go mod tidy` fails because an upstream `bu/govips` test imports a
removed `davidbyttow/govips` package. Use `go mod tidy -e` if refreshing the
module graph. The separate Go 1.27.1 standard-library inventory records no
PNM-aware parser API.

`verify_python_png.py` uses CPython 3.13.1 and the two valid local PNG
controls. `requirements.in` pins 21 top-level releases; the generated
`requirements.lock` pins transitive versions and distribution hashes. The
recorded result is **21/21 third-party packages passing**. Pixel decoders,
dimension readers, chunk readers, and a `tEXt` metadata reader have separate
scopes in the ranking. Several packages call Pillow, ImageIO, libvips, or
other native image engines. The run used uv 0.12.19, libvips 8.18.7, and
ImageMagick 7.1.2; the latter two need installed shared libraries. The
verifier sets `MAGICK_HOME` from `pkg-config` for Wand. The Python 3.13
standard/runtime inventory separately verifies Tkinter `PhotoImage` with
bundled Tk 8.6 on the same valid control; it requires a usable GUI session.

`verify_python_ascii_pnm.py` uses the valid 2×1 ASCII P3 red/green PPM and
P2 black/white PGM controls. The pinned, hash-locked Python 3.13 environment
reproduces **20/20 package paths passing**. Eighteen expose P3 pixels, one
exposes P2 grayscale pixels, and one parses P3 header dimensions only. They
include wrappers over Pillow, Qt, and netpbmfile; those shared families are
labeled in the ranking. The verifier also probes bundled Tk 8.6 `PhotoImage`
on valid P1/P2/P3 files and records its three rejections separately from the
package count. `pyvips` and Wand need libvips and ImageMagick shared libraries,
and wxPython/Tk need a GUI session. `napari-netpbmfile` omits a declared
`napari-plugin-engine` dependency; it is pinned explicitly in
`requirements.in`.

`verify_python_zip.py` verifies **20/20 third-party package paths** and
**4/4 CPython standard-library APIs** on valid local ZIP controls. The main
control has a DEFLATE-compressed `hello.txt`; the pinned Zstandard wrapper
generates and reads a method-93 ZIP, and a separate Python-module ZIP tests
`zipimport`. Many packages share CPython's `zipfile` parser family; the
ranking lists those families. `libarchive-c` needs a libarchive shared library,
`patool` needs a local `unzip` utility, and `fs` and `omni-archive` need the
explicit compatibility pins in `requirements.in` for this Python version.

`verify_python_wav.py` verifies **21/21 third-party package paths** and
**1/1 CPython standard-library API** using the four-sample PCM16 WAV control.
The pinned Python 3.13 environment has distribution hashes in
`requirements.lock`. The ranking labels sample readers and WAV metadata
readers, and identifies packages that share CPython `wave`, libsndfile,
FFmpeg, or other backends. Pygame uses a dummy SDL audio driver for its
control run. The standard-library result is `wave.open`.

`verify_python_pdf.py` verifies **20/20 third-party package paths** on the
one-page PDF control. Eighteen packages share the main hash-locked Python 3.13
environment; PDFx and Slate3k use isolated locks because their older
`pdfminer` dependencies conflict with current `pdfminer.six`. The
`pdf2image` and `pdftotext` paths require a local Poppler installation;
the recorded host used Poppler 26.09.0. The ranking distinguishes text,
metadata, layout, and page-rendering results and names shared parser engines.
The scoped CPython standard-library inventory found no PDF-aware input API.

To refresh *discovery and popularity* data, run
`node scripts/snapshot_npm.mjs png`, `zip`, `mp4`, `mp3_id3v2`, `wav`, `pdf`, `svg`, or `http11`.
Run `node scripts/triage_npm.mjs png`, `zip`, `mp4`, `mp3_id3v2`, `wav`, `pdf`, `svg`, or `http11`
to refresh popularity-sorted **leads**; triage never verifies a parser.
This is a separate, network-dependent operation that changes the dated registry
snapshot; verification itself uses only locked local dependencies. npm's
[search API](https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md)
supplies discovery hits. Its [downloads API](https://github.com/npm/registry/blob/main/docs/download-counts.md)
supplies the single ranking metric. The metric is the number of registry
downloads during **2026-10-11 through 2026-11-09**, inclusive, for each package
name. It is an adoption proxy and can include automated downloads.

For Go ZIP, PNG, WAV, HTTP/1.1, MP4, MP3 with ID3v2, PDF, SVG, or ASCII PNM discovery, install the pinned packages in
`scripts/requirements-go-discovery.txt`, then run `python3 scripts/snapshot_go.py FORMAT`
and `python3 scripts/enrich_go.py FORMAT` with `FORMAT` set to `zip`, `png`,
`wav`, `http11`, `mp4`, `mp3_id3v2`, `pdf`, `svg`, or `ascii_pnm`. These refresh bounded pkg.go.dev
package-search hits, pinned-release license evidence, and package-level
“Imported by” counts. Go counts are compared only within their Go format cell.
The public search pages supplied this snapshot after the
[pkg.go.dev API](https://pkg.go.dev/v1/api) returned a rate limit response.

For Python PNG, ASCII PNM, ZIP, WAV, or PDF discovery, run
`python3 scripts/snapshot_pypi_png.py`,
`python3 scripts/snapshot_pypi_ascii_pnm.py`, or
`python3 scripts/snapshot_pypi_zip.py`, or
`python3 scripts/snapshot_pypi_wav.py`, or
`python3 scripts/snapshot_pypi_pdf.py`. Each
filters the [PyPI Simple JSON project index](https://docs.pypi.org/api/index-api/)
by recorded name terms, saves the first 100 alphabetic matches per term, and
fetches pinned release metadata. [PyPI Stats](https://pypistats.org/api/)
provides its `last_month` download signal, excluding known mirrors. The
index is not relevance ranked, and the download signal is compared only
within Python. Unavailable metrics remain `null`.

## Verified rankings and search limits

The working goal is 20 verified third-party parsers per cell, with 30 as the
original ceiling. The JavaScript PNG and ZIP cells have **21 verified packages** each;
the WAV, PDF, and SVG cells have **22** each, MP4 and HTTP/1.1 have **20** each,
and MP3 with ID3v2 has **24**.
Packages verified after the twentieth row are kept in
the collection. Package downloads are an adoption proxy, not a security
or quality judgment.

- [JavaScript × PNG ranking](data/javascript/png/ranking.md): 21 packages,
  including header-only and chunk-only parsers labeled by scope. Four npm queries
  saved the first 100 results each: 400 hits, 344 unique names. Ten named leads
  remain unresolved. The [runtime inventory](data/javascript/png/standard.json)
  separately verifies browser `createImageBitmap(Blob)` and records the scoped
  Node.js 26.10.0 built-in API finding. The browser API is specified by the
  [HTML Standard](https://html.spec.whatwg.org/multipage/imagebitmap-and-animations.html#dom-createimagebitmap-dev).
- [JavaScript × ZIP ranking](data/javascript/zip/ranking.md): 21 packages, each
  returning the entry name and decompressed text. Four npm queries saved the
  first 100 results each: 400 hits, 314 unique names. Four named leads remain
  unresolved. The [Node.js `zlib.ZipBuffer` API](https://nodejs.org/docs/v26.10.0/api/zlib.html#class-zlibzipbuffer)
  is experimental and verified separately from the npm ranking.
- [JavaScript × MP4 ranking](data/javascript/mp4/ranking.md): 20 packages with
  labeled box, metadata, track, or audio decode scope. Five npm queries saved
  the first 100 hits each: 500 hits, 372 unique names. Fifteen named leads
  remain unresolved. The browser `HTMLVideoElement` metadata API is verified
  separately with a local MP4 Blob; see the
  [runtime inventory](data/javascript/mp4/standard.json).
- [JavaScript × MP3 with ID3v2 ranking](data/javascript/mp3_id3v2/ranking.md):
  24 packages with tag, audio decode, or duration scope. Five npm queries saved
  495 hits, 447 unique names; the first query returned only 95 hits and the
  other four stopped at 100. Ten named leads remain unresolved. The
  [runtime inventory](data/javascript/mp3_id3v2/standard.json) separately
  verifies browser audio decoding and media metadata on the tagged control.
- [JavaScript × WAV ranking](data/javascript/wav/ranking.md): 22 packages with
  explicitly labeled sample, header, or duration scope. Four npm queries saved
  the first 100 results each: 400 hits, 351 unique names. Five relevant leads
  remain unresolved. The separate [runtime inventory](data/javascript/wav/standard.json)
  verifies Chromium's `OfflineAudioContext.decodeAudioData(ArrayBuffer)` on the
  same control, using the [Web Audio specification](https://www.w3.org/TR/webaudio-1.1/#dom-baseaudiocontext-decodeaudiodata).
- [JavaScript × PDF ranking](data/javascript/pdf/ranking.md): 22 packages,
  including text extraction, page metadata, and page count APIs. Four npm queries
  saved the first 100 results each: 400 hits, 347 unique names. Twelve relevant
  leads remain unresolved. Shared PDF.js wrappers are grouped by family. The
  [runtime inventory](data/javascript/pdf/standard.json) documents the scoped
  absence of a public PDF parsing API in Node.js core and browser standards.
- [JavaScript × HTTP/1.1 ranking](data/javascript/http11/ranking.md): 20 packages
  parsing a request or response control. Six npm queries saved the first 100
  results each: 600 hits, 268 unique names. Eight named leads remain unresolved.
  The [runtime inventory](data/javascript/http11/standard.json) separately
  verifies Node.js `node:http.createServer` using the local request bytes.
- [JavaScript × SVG ranking](data/javascript/svg/ranking.md): 22 packages
  spanning structure, dimensions, colors, paths, and rendered pixels. Four npm
  queries saved 400 hits, 388 unique names. Twelve named leads remain
  unresolved. The [runtime inventory](data/javascript/svg/standard.json)
  separately verifies browser SVG DOM parsing and image decoding.
- [Go × ZIP ranking](data/go/zip/ranking.md): 23 packages spanning direct ZIP
  readers, streaming readers, and extraction wrappers. Five pkg.go.dev queries
  saved 333 hits, 271 unique package paths. Eight named leads remain
  unresolved. The [standard-library inventory](data/go/zip/standard.json)
  separately verifies `archive/zip.OpenReader` on the same control.
- [Go × PNG ranking](data/go/png/ranking.md): 20 packages spanning pixel,
  chunk, and dimension readers. Five pkg.go.dev queries saved 321 hits and
  228 unique package paths. Five named leads remain unresolved. The
  [standard-library inventory](data/go/png/standard.json) separately verifies
  `image/png.Decode`, `DecodeConfig`, and registered `image.Decode`.
- [Go × WAV ranking](data/go/wav/ranking.md): 21 packages with labeled sample,
  header, and data-size scopes. Five pkg.go.dev queries saved 373 hits and
  271 unique package paths; eight named leads remain unresolved. The
  [standard-library inventory](data/go/wav/standard.json) records the scoped
  Go 1.27.1 finding.
- [Go × HTTP/1.1 ranking](data/go/http11/ranking.md): 20 packages with labeled
  request-message, header, and request-line scopes. Six pkg.go.dev queries saved
  404 hits and 364 unique package paths; ten named leads remain unresolved.
  The [standard-library inventory](data/go/http11/standard.json) separately
  verifies `net/http.ReadRequest` and `ReadResponse`.
- [Go × MP4 ranking](data/go/mp4/ranking.md): 20 packages with labeled box,
  track, stream, and title scopes. Five pkg.go.dev queries saved 133 hits and
  124 unique package paths; ten plausible leads remain unresolved, including
  fragmented-MP4 readers requiring a separate valid control. The
  [standard-library inventory](data/go/mp4/standard.json) records the scoped
  Go 1.27.1 finding.
- [Go × MP3 with ID3v2 ranking](data/go/mp3_id3v2/ranking.md): 20 packages with
  labeled audio, MPEG frame, duration, and ID3 title scopes. Five pkg.go.dev
  queries saved 311 hits and 252 unique package paths; ten plausible leads
  remain unresolved. The [standard-library inventory](data/go/mp3_id3v2/standard.json)
  records the scoped Go 1.27.1 finding.
- [Go × PDF ranking](data/go/pdf/ranking.md): 20 packages with labeled page,
  text, version, or object scope. Five pkg.go.dev queries saved 462 hits and
  384 unique package paths; ten plausible leads remain unresolved, including
  a native PDFium binding and a reader that failed to compile with the pinned
  pdfcpu version. The [standard-library inventory](data/go/pdf/standard.json)
  records the scoped Go 1.27.3 finding.
- [Go × SVG ranking](data/go/svg/ranking.md): 21 packages with labeled shape,
  path, viewBox, raster, or SVG minification scope. Five pkg.go.dev queries saved
  322 hits and 280 unique package paths; ten plausible leads remain unresolved.
  One higher-adoption reader could not link because the host lacked MoltenVK.
  The [standard-library inventory](data/go/svg/standard.json) records the scoped
  Go 1.27.1 finding.
- [Go × ASCII PNM ranking](data/go/ascii_pnm/ranking.md): 20 packages verified
  on the valid P3 control, with pixels, dimensions, or header fields as labeled.
  Five pkg.go.dev queries saved 156 hits and 141 unique package paths; ten
  plausible leads remain unresolved. Five accepted bindings share libvips,
  and several modules share Go PNM code. The
  [standard-library inventory](data/go/ascii_pnm/standard.json) records the
  scoped Go 1.27.1 finding.
- [Python × PNG ranking](data/python/png/ranking.md): 21 packages verified
  on local pixel or text-chunk controls. Seven bounded PyPI name filters
  saved 379 distinct project names; eight plausible leads remain unresolved.
  One verified package lacks a PyPI Stats figure and is left unranked. The
  [standard/runtime inventory](data/python/png/standard.json) separately
  verifies Tkinter `PhotoImage` and records its platform limit.
- [Python × ASCII PNM ranking](data/python/ascii_pnm/ranking.md): 20 package
  paths verified on valid P3 or P2 controls, with pixel or header scopes
  labeled. Twelve bounded PyPI name filters saved 675 hits and 669 distinct
  project names; six plausible leads remain unresolved. One verified package
  initially hit a PyPI Stats rate limit; a successful retry supplied its figure. The
  [standard/runtime inventory](data/python/ascii_pnm/standard.json) records
  Tkinter's failed ASCII controls and the scoped CPython finding.
- [Python × ZIP ranking](data/python/zip/ranking.md): 20 package paths verified
  on valid DEFLATE or Zstandard ZIP controls. Nine bounded PyPI name filters
  saved 418 hits and 407 distinct names; six plausible leads remain unresolved.
  The higher-download `zipfile-deflate64` lead failed to build on this host and
  was not counted. The [standard/runtime inventory](data/python/zip/standard.json)
  separately verifies four documented CPython API paths.
- [Python × WAV ranking](data/python/wav/ranking.md): 21 package paths verified
  on the PCM16 control, with sample and metadata scopes labeled. Nine bounded
  PyPI name filters saved 782 hits and 688 distinct names; five plausible
  leads remain unresolved, including torchaudio. The
  [standard-library inventory](data/python/wav/standard.json) separately
  verifies `wave.open`.
- [Python × PDF ranking](data/python/pdf/ranking.md): 20 package paths verified
  on the valid one-page control. Nine bounded PyPI name filters saved 677
  hits and 672 distinct names; nine plausible leads remain unresolved. Shared
  PDF engines are labeled, and the
  [standard-library inventory](data/python/pdf/standard.json) records the
  scoped absence of a CPython PDF parser API.

The full discovery surfaces have not been exhausted. The [PNG cell record](data/javascript/png/cell.json)
and [ZIP cell record](data/javascript/zip/cell.json), along with the
[WAV cell record](data/javascript/wav/cell.json) and
[PDF cell record](data/javascript/pdf/cell.json), and
[HTTP/1.1 cell record](data/javascript/http11/cell.json), and
[SVG cell record](data/javascript/svg/cell.json), and
[MP4 cell record](data/javascript/mp4/cell.json), and
[MP3 with ID3v2 cell record](data/javascript/mp3_id3v2/cell.json) state the actual counts,
search limits, and remaining uncertainty. Registry hits and download counts are
not parser evidence; only the pinned APIs and successful control runs enter the
rankings.
The [Go ZIP cell record](data/go/zip/cell.json) gives its separate count,
search limits, and uncertainty.
The [Go PNG cell record](data/go/png/cell.json) gives the corresponding
PNG-specific limits and uncertainty.
The [Go WAV cell record](data/go/wav/cell.json) gives the WAV search limits and
uncertainty.

## Data layout

- `data/cells.json`: every ecosystem × format cell, with status, actual verified
  count, search limit, and uncertainty.
- `data/go/zip/`: bounded pkg.go.dev search hits, pinned module and license
  evidence, package importer counts, verified ranking, leads, standard API,
  and control results. `adapters/go/zip/go.mod` and `go.sum` pin dependencies.
- `data/go/png/`: the same evidence layout for Go PNG; native libvips and
  MagickWand dependencies are stated above.
- `data/go/wav/`: bounded registry search, pinned releases, per-package WAV
  control outputs, ranking, leads, and the separate standard-library finding.
- `data/go/ascii_pnm/`: bounded search hits, pinned releases, package-level
  importer counts, P3 control outputs, ranking, leads, and standard-library
  finding. Native adapters live under `adapters/go/ascii_pnm/`.
- `data/python/png/`: PyPI name-index leads, pinned release hashes,
  within-Python download signals, verified ranking, standard-library
  inventory, and control outputs. Python dependencies and the adapter live
  under `adapters/python/png/`.
- `data/python/ascii_pnm/`: the same evidence layout for ASCII PNM, with
  P3/P2 control output and the Tk runtime candidate result. Python adapters
  and pinned dependencies live under `adapters/python/ascii_pnm/`.
- `data/python/zip/`: bounded PyPI leads, pinned release hashes, within-Python
  download counts, a verified ranking, control outputs, and four standard APIs.
  The adapters and dependency lock live under `adapters/python/zip/`.
- `data/python/wav/`: bounded PyPI leads, pinned release hashes, within-Python
  downloads, sample and metadata scopes, control outputs, and the separate
  standard-library result. The adapters and lock live under
  `adapters/python/wav/`.
- `data/python/pdf/`: bounded PyPI leads, three pinned Python environments,
  within-Python downloads, verified text/metadata/layout/rendering scopes,
  control outputs, and the separate standard-library finding.
- `data/javascript/{png,zip,mp4,mp3_id3v2,wav,pdf,svg,http11}/registry-snapshot.json`: dated registry hits, pinned
  release metadata, and comparable download counts. A hit is not verification.
- `data/javascript/{png,zip,mp4,mp3_id3v2,wav,pdf,svg,http11}/triage.json`: popularity-sorted discovery leads,
  including unresolved names; the status distinguishes verified packages.
- `data/javascript/{png,zip,mp4,mp3_id3v2,wav,pdf,svg,http11}/parsers.json`: pinned packages, documented input APIs,
  parsing depth, licenses, and shared families.
- `data/javascript/{png,zip,mp4,mp3_id3v2,wav,pdf,svg,http11}/ranking.md`: generated rankings using only verified
  package rows and the recorded metric window.
- `adapters/javascript/` and `controls/`: runnable local-input adapters and
  deterministic valid controls.
- `data/javascript/{png,zip,mp4,mp3_id3v2,wav,pdf,svg,http11}/verification.json` and `png/browser-verification.json`:
  observed outputs, environment, and pass/fail result.

This collection does not contain malformed-input, security, or resource-use
experiments.
