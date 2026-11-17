# HTMLAudioElement.src = URL.createObjectURL(Blob({type:audio/mpeg})); loadedmetadata; duration — MP3 / JavaScript browser

This container pins Chromium 153.0.8010.12 and Playwright 1.63.0. It feeds a local valid control to the documented browser API and records its parsed result.

[API and catalog evidence](../../../../catalog/mp3/javascript/standard/htmlaudioelement-src-url-createobjecturl-blob-type-audio-mpeg-loadedmetadata-duration/README.md) · [runtime lock](runtime-lock.json) · [control receipt](control-verification.json)

## Build and check the valid control

From the repository root:

```sh
python3 projects/mp3/javascript/stdlib_browser_audio_metadata/verify-control.py
```

## Replay another file

```sh
docker run --rm --platform linux/arm64 --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,exec,nosuid,size=256m --shm-size=256m \
  -e HOME=/tmp -v "$PWD/controls/mp3/id3v2-tagged-tone.mp3:/input/file:ro" \
  --entrypoint node parsarium/mp3-javascript-stdlib_browser_audio_metadata:local \
  /work/replay.mjs /input/file
```

Replace the mounted path to replay another file of this format. `replay.mjs -` also accepts bytes from standard input.

The control receipt records V8 coverage of the JavaScript harness only. Chromium's native format decoder source and AFL++ parser feedback are unavailable in this image, so this path is staged rather than counted as fully instrumented.
