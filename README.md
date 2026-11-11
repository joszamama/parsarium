# Parsarium

Parsarium is a reproducible catalogue of libraries and bundled APIs that parse
specific formats. It currently contains a verified JavaScript × PNG pilot,
JavaScript × ZIP and WAV batches, and an explicit 88-cell work matrix. The other 85 cells
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
npm run wav:control
npm run wav:verify
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

To refresh *discovery and popularity* data, run
`node scripts/snapshot_npm.mjs png`, `zip`, or `wav`.
Run `node scripts/triage_npm.mjs png`, `zip`, or `wav`
to refresh popularity-sorted **leads**; triage never verifies a parser.
This is a separate, network-dependent operation that changes the dated registry
snapshot; verification itself uses only locked local dependencies. npm's
[search API](https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md)
supplies discovery hits. Its [downloads API](https://github.com/npm/registry/blob/main/docs/download-counts.md)
supplies the single ranking metric. The metric is the number of registry
downloads during **2026-10-11 through 2026-11-09**, inclusive, for each package
name. It is an adoption proxy and can include automated downloads.

## Verified rankings and search limits

The working goal is 20 verified third-party parsers per cell, with 30 as the
original ceiling. The PNG and ZIP cells have **21 verified packages** each;
the WAV cell has **22**. Packages verified after the twentieth row are kept in
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
- [JavaScript × WAV ranking](data/javascript/wav/ranking.md): 22 packages with
  explicitly labeled sample, header, or duration scope. Four npm queries saved
  the first 100 results each: 400 hits, 351 unique names. Five relevant leads
  remain unresolved. The separate [runtime inventory](data/javascript/wav/standard.json)
  verifies Chromium's `OfflineAudioContext.decodeAudioData(ArrayBuffer)` on the
  same control, using the [Web Audio specification](https://www.w3.org/TR/webaudio-1.1/#dom-baseaudiocontext-decodeaudiodata).

The full discovery surfaces have not been exhausted. The [PNG cell record](data/javascript/png/cell.json)
and [ZIP cell record](data/javascript/zip/cell.json), along with the
[WAV cell record](data/javascript/wav/cell.json), state the actual counts,
search limits, and remaining uncertainty. Registry hits and download counts are
not parser evidence; only the pinned APIs and successful control runs enter the
rankings.

## Data layout

- `data/cells.json`: every ecosystem × format cell, with status, actual verified
  count, search limit, and uncertainty.
- `data/javascript/{png,zip,wav}/registry-snapshot.json`: dated registry hits, pinned
  release metadata, and comparable download counts. A hit is not verification.
- `data/javascript/{png,zip,wav}/triage.json`: popularity-sorted discovery leads,
  including unresolved names; the status distinguishes verified packages.
- `data/javascript/{png,zip,wav}/parsers.json`: pinned packages, documented input APIs,
  parsing depth, licenses, and shared families.
- `data/javascript/{png,zip,wav}/ranking.md`: generated rankings using only verified
  package rows and the recorded metric window.
- `adapters/javascript/` and `controls/`: runnable local-input adapters and
  deterministic valid controls.
- `data/javascript/{png,zip,wav}/verification.json` and `png/browser-verification.json`:
  observed outputs, environment, and pass/fail result.

This collection does not contain malformed-input, security, or resource-use
experiments.
