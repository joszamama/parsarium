# Parsarium

Parsarium is a reproducible catalogue of libraries and bundled APIs that parse
specific formats. It currently contains a verified JavaScript × PNG pilot,
JavaScript × ZIP, MP4, WAV, PDF, SVG, HTTP/1.1, and MP3 with ID3v2 batches,
Go × ZIP, and an explicit 88-cell work matrix. The other 79 cells
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

For Go ZIP discovery, install the pinned packages in
`scripts/requirements-go-discovery.txt`, then run `python3 scripts/snapshot_go.py zip`
and `python3 scripts/enrich_go.py zip`. These refresh bounded pkg.go.dev
package-search hits, pinned-release license evidence, and package-level
“Imported by” counts. Go counts are compared only with other Go ZIP packages.
The public search pages supplied this snapshot after the
[pkg.go.dev API](https://pkg.go.dev/v1/api) returned a rate limit response.

## Verified rankings and search limits

The working goal is 20 verified third-party parsers per cell, with 30 as the
original ceiling. The PNG and ZIP cells have **21 verified packages** each;
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

## Data layout

- `data/cells.json`: every ecosystem × format cell, with status, actual verified
  count, search limit, and uncertainty.
- `data/go/zip/`: bounded pkg.go.dev search hits, pinned module and license
  evidence, package importer counts, verified ranking, leads, standard API,
  and control results. `adapters/go/zip/go.mod` and `go.sum` pin dependencies.
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
