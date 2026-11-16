# createImageBitmap(Blob) — PNG / JavaScript browser

This container pins Chromium 153.0.8010.12 and Playwright 1.63.0. It sends a local PNG file to the browser as a `Blob`, calls `createImageBitmap`, then reads the decoded size and RGBA pixels from a canvas.

[API and catalog evidence](../../../../catalog/png/javascript/standard/createimagebitmap-blob/README.md) · [runtime lock](runtime-lock.json) · [control receipt](control-verification.json)

## Build and check the valid control

From the repository root:

```sh
python3 projects/png/javascript/stdlib_browser_createimagebitmap_blob/verify-control.py
```

## Replay another PNG

```sh
docker run --rm --platform linux/arm64 --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,exec,nosuid,size=256m --shm-size=256m \
  -e HOME=/tmp -v "$PWD/controls/png/red-green.png:/input/file:ro" \
  --entrypoint node \
  parsarium/png-javascript-stdlib_browser_createimagebitmap_blob:local \
  /work/replay.mjs /input/file
```

Replace the mounted PNG path to replay another file. `replay.mjs -` also accepts bytes from standard input.

The control receipt records V8 coverage of the JavaScript harness only. Chromium's native PNG decoder source and AFL++ parser feedback are unavailable in this image, so this path is staged rather than counted as fully instrumented.
