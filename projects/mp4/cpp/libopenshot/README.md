# libopenshot — MP4 / C++

Pinned release: `1.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/cpp/libopenshot/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 cpp libopenshot
python3 parsarium.py run mp4 cpp libopenshot controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 cpp libopenshot CORPUS_DIR runs/mp4-libopenshot-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build mp4 cpp libopenshot
python3 parsarium.py afl prepare mp4 cpp libopenshot runs/mp4-libopenshot-afl --fandango 100
python3 parsarium.py afl run runs/mp4-libopenshot-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.

**Coverage limit:** libopenshot's FFmpegReader opens media through libavformat, so it shares the FFmpeg MOV/MP4 parser family with the FFmpeg, MLT, and other FFmpeg-backed targets. The minimal Docker build enables only the H.264 and AAC decoders the control needs; other codecs leave codec fields null or disable the stream. AFL++ runs one process per local MP4 file through the replay binary.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
