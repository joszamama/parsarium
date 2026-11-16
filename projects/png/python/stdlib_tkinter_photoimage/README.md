# tkinter.PhotoImage — PNG / Python

This container builds CPython 3.13.1 and Tk 8.6.16 from pinned source. Xvfb provides a display while `tkinter.PhotoImage(file=...)` parses a local PNG. The control reads dimensions and both pixel colors.

[API and catalog evidence](../../../../catalog/png/python/standard/tkinter-photoimage-file-local-path-width-height-get-x-y/README.md) · [runtime lock](runtime-lock.json) · [control receipt](control-verification.json)

## Build and check the valid control

From the repository root:

```sh
python3 projects/png/python/stdlib_tkinter_photoimage/verify-control.py
```

## Replay another PNG

```sh
docker run --rm --platform linux/arm64 --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,exec,nosuid,size=256m \
  -v "$PWD/controls/png/red-green.png:/input/file:ro" \
  --entrypoint /opt/python/bin/python3.13 \
  parsarium/png-python-stdlib_tkinter_photoimage:local \
  /work/replay-cli.py /input/file
```

Replace the mounted path to replay another PNG. The control receipt records covered lines in Tk's native `tkImgPNG.c` reader. The [AFL++ feedback overlay](../../../../fuzzing/afl-native/png/python/stdlib_tkinter_photoimage/README.md) recompiles the pinned Tk PNG decoder and checks two valid PNGs for stable, format-sensitive feedback.
