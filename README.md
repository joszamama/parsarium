# Parsarium

Parsarium is a reproducible catalogue of libraries and bundled APIs that parse
specific formats. It currently contains a verified JavaScript × PNG pilot, a
JavaScript × ZIP batch, and an explicit 88-cell work matrix. The other 86 cells
are marked `not_started`;
a zero in those cells does **not** mean no parser exists. See the
[selection protocol](PROTOCOL.md) before adding a package.

## Reproduce the pilot

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
python3 scripts/build_matrix.py
python3 scripts/validate_catalog.py
```

`pilot:control` generates the 71-byte PNG in `controls/png/red-green.png` with
SHA-256 `5a852fbaaaecaf4cd14c01e150c7f881c5c5894b0a1e3c53be7e007c58374ee6`.
It has two opaque pixels: red and green. The verifier runs each package adapter
against the path, checks parsed dimensions and either decoded pixels, parsed
chunks, or the format-bearing header result, then writes dated JSON results.
It also runs the browser-bundled `createImageBitmap(Blob)` adapter with the same
control. The observed pilot result is **12/12 third-party packages and 1/1
runtime API passing**. A fresh run replaces the dated result files.

`zip:control` creates a deterministic 128-byte ZIP with one DEFLATE-compressed
`hello.txt` entry containing `parsarium\n` (SHA-256
`c534fa083d1da92474852ca9168ba0793740c25205f828915a1d862bd78c776b`).
The ZIP adapter checks both the parsed entry name and decompressed content.
The observed batch result is **8/8 third-party packages and 1/1 Node.js
built-in API passing**.

To refresh *discovery and popularity* data, run
`node scripts/snapshot_npm.mjs png` or `node scripts/snapshot_npm.mjs zip`.
This is a separate, network-dependent operation that changes the dated registry
snapshot; verification itself uses only locked local dependencies. npm's
[search API](https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md)
supplies discovery hits. Its [downloads API](https://github.com/npm/registry/blob/main/docs/download-counts.md)
supplies the single ranking metric. The metric is the number of registry
downloads during **2026-10-11 through 2026-11-09**, inclusive, for each package
name. It is an adoption proxy and can include automated downloads.

## Pilot ranking: JavaScript × PNG

Only packages with a successful control run appear here. Header-only and
chunk-only parsers are labeled because they do less than pixel decoders.
Shared families are recorded so rows are not mistaken for independent parsers.

| Rank | Package (pinned) | Downloads in window | Scope | Underlying family |
| ---: | --- | ---: | --- | --- |
| 1 | sharp 0.35.5 | 556,685,199 | pixels | libvips |
| 2 | pngjs 7.0.0 | 349,449,466 | pixels | pngjs |
| 3 | image-size 2.1.0 | 139,419,348 | header | image-size |
| 4 | @pdf-lib/upng 1.0.1 | 105,408,220 | pixels | UPNG.js |
| 5 | png-js 2.0.0 | 71,464,407 | pixels | png.js |
| 6 | fast-png 8.0.0 | 68,006,004 | pixels | fast-png |
| 7 | parse-png 2.1.0 | 52,308,135 | pixels | pngjs |
| 8 | jimp 1.6.1 | 15,092,580 | pixels | pngjs |
| 9 | @react-pdf/png-js 3.0.0 | 10,632,241 | pixels | png.js |
| 10 | png-chunks-extract 1.0.0 | 4,817,936 | chunks | png-chunks-extract |
| 11 | upng-js 2.1.0 | 1,894,825 | pixels | UPNG.js |
| 12 | @jsquash/png 3.1.1 | 1,685,572 | pixels | Rust png crate via WASM |

The registry snapshot contains four queries (`png`, `png decoder`, `png reader`,
`png image`), capped at the first 30 results each: 120 hits, 109 unique names.
This is a **partial search**, not a claim that twelve exhaust the cell. Six
relevant leads await a documented standalone API and/or a control run; other
packages may lie beyond the saved result windows. See
[`cell.json`](data/javascript/png/cell.json) and
[`leads.json`](data/javascript/png/leads.json) for exact limits and dispositions.

The [runtime inventory](data/javascript/png/standard.json) records one verified
browser API and the scoped finding that Node.js 26.10.0 documents no built-in
PNG parser. Browser `createImageBitmap` is specified by the
[HTML Standard](https://html.spec.whatwg.org/multipage/imagebitmap-and-animations.html#dom-createimagebitmap-dev).
Other browser engines and JavaScript runtimes remain open.

## Batch 1 ranking: JavaScript × ZIP

These eight packages all returned the entry name and decompressed text from the
same ZIP control. Counts use the same 2026-10-11 through 2026-11-09 npm window.

| Rank | Package (pinned) | Downloads in window | Underlying family |
| ---: | --- | ---: | --- |
| 1 | fflate 0.8.3 | 510,564,404 | fflate |
| 2 | yauzl 3.4.0 | 250,080,200 | yauzl |
| 3 | jszip 3.10.2 | 240,876,211 | JSZip |
| 4 | unzipper 0.12.5 | 132,565,324 | unzipper |
| 5 | adm-zip 0.6.1 | 108,718,725 | ADM-ZIP |
| 6 | extract-zip 2.0.1 | 102,046,075 | yauzl |
| 7 | @zip.js/zip.js 2.24.0 | 29,998,288 | zip.js |
| 8 | node-stream-zip 1.16.0 | 28,433,168 | node-stream-zip |

The four ZIP searches saved 120 hits, 98 unique names, with a limit of 30 per
query. Two named leads remain unresolved, and most registry hits were not
reviewed. This is a partial ranking; see [`cell.json`](data/javascript/zip/cell.json)
for the exact limits. The [Node.js ZIP API](https://nodejs.org/docs/v26.10.0/api/zlib.html#class-zlibzipbuffer)
is built in and verified separately. It is experimental in Node.js 26.10.0.

## Data layout

- `data/cells.json`: every ecosystem × format cell, with status, actual verified
  count, search limit, and uncertainty.
- `data/javascript/{png,zip}/registry-snapshot.json`: dated registry hits, pinned
  release metadata, and comparable download counts. A hit is not verification.
- `data/javascript/{png,zip}/parsers.json`: pinned packages, documented input APIs,
  parsing depth, licenses, and shared families.
- `adapters/javascript/` and `controls/`: runnable local-input adapters and
  deterministic valid controls.
- `data/javascript/{png,zip}/verification.json` and `png/browser-verification.json`:
  observed outputs, environment, and pass/fail result.

This collection does not contain malformed-input, security, or resource-use
experiments.
