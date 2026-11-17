# macOS Core Graphics CGPDFDocument — PDF / C

This path runs on a macOS host, not in Docker. Core Graphics is a closed Apple system framework and does not run in a Linux image. `replay.c` opens a local file with `CGPDFDocumentCreateWithURL` and prints the page count as JSON.

[API and catalog evidence](../../../../catalog/pdf/c/standard/macos-core-graphics-cgpdfdocument/README.md) · [evidence adapter](../../../../adapters/c/pdf/coregraphics.c) · [manifest](macos-manifest.json) · [control receipt](control-verification.json)

## Build and check the valid control

From the repository root on macOS:

```sh
python3 projects/pdf/c/stdlib_coregraphics/verify-control.py
```

This builds the replay, checks the toolchain pins, runs `controls/pdf/one-page.pdf` through the replay and the evidence adapter, and rewrites the receipt. It only succeeds on the pinned host: macOS 27.2 (26B123) on arm64, Command Line Tools 27.2.0.0.1792721180, MacOSX 27.2 SDK (26B118), and Apple clang 21.0.0 (clang-2100.4.1.1). Xcode is not required.

## Replay another file

```sh
projects/pdf/c/stdlib_coregraphics/build-macos.sh
projects/pdf/c/stdlib_coregraphics/target/coregraphics-replay path/to/file.pdf
```

On a different macOS version or SDK, build with `PARSARIUM_ALLOW_UNPINNED=1`. The replay works, but the receipt does not apply to that build.

Exit codes: `0` prints `{"pages":N}`; `1` usage; `2` path not convertible to a URL; `3` Core Graphics rejected the document; `4` zero pages.

## Limits

The receipt proves the valid control only. Core Graphics source is not public, so there is no parser source coverage. A pinned [AFL++ Frida probe](feedback-blocker.json) found no reliable Core Graphics scoped feedback on two valid PDFs; this path stays staged.
