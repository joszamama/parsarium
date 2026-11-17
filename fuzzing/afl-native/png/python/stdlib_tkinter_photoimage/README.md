# Tkinter PhotoImage PNG decoder feedback

This overlay rebuilds the pinned Tk 8.6.16 `tkImgPNG.c` source with AFL++ 4.33c. The source allowlist limits AFL instrumentation to that PNG decoder. It uses the verified CPython 3.13.1 control image as its base, so the Python and Tcl/Tk runtime remain pinned.

From the repository root:

```sh
python3 projects/png/python/stdlib_tkinter_photoimage/verify-control.py
python3 fuzzing/afl-native/png/python/stdlib_tkinter_photoimage/verify-feedback.py
```

The second command checks both valid PNG controls through `tkinter.PhotoImage(file=...)` under Xvfb. It confirms native decoder source coverage, repeats AFL++ maps to check stability, and requires a different map for the valid `tEXt` chunk variant. The [feedback receipt](verification.json) records the pinned images, hashes, line coverage, and edge counts.

To replay another PNG with the instrumented Tk build:

```sh
docker run --rm --platform linux/arm64 --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --tmpfs /tmp:rw,exec,nosuid,size=256m \
  -v "$PWD/controls/png/red-green.png:/input/file:ro" \
  parsarium-afl/png-python-stdlib_tkinter_photoimage:local /input/file
```

This preparation checks feedback on valid files. It does not start a mutation campaign.
