# mlt — MP4 / C

Pinned release: `7.42.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/c/mlt/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 c mlt
python3 parsarium.py run mp4 c mlt controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 c mlt CORPUS_DIR runs/mp4-mlt-replay
python3 parsarium.py afl build mp4 c mlt
python3 parsarium.py afl prepare mp4 c mlt runs/mp4-mlt-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** MLT C and C++ paths share the avformat plugin and FFmpeg MOV/MP4 parser family. The minimal Docker build enables H.264 and AAC decoders for the control, with null codec fields possible for other codecs. AFL++ runs one process per local MP4 file because MLT loads and closes global plugins.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
