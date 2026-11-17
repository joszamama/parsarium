# MLT — MP4 / C

Pinned releases: MLT `7.42.0` and FFmpeg `9.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/c/mlt/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 c mlt
python3 parsarium.py run mp4 c mlt controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 c mlt CORPUS_DIR runs/mp4-mlt-replay
python3 parsarium.py afl build mp4 c mlt
python3 parsarium.py afl prepare mp4 c mlt runs/mp4-mlt-afl
```

Replace `CORPUS_DIR` with a directory of MP4 files. The AFL++ command prepares a seeded run; it does not start a campaign.

The harness gives a local `.mp4` file to MLT's public `mlt_factory_producer(..., "avformat", path)` C API and reports stream count, codec names, and video dimensions. Its avformat plugin reaches FFmpeg's `mov.c` parser. The C and C++ MLT paths share this plugin and underlying FFmpeg parser family.

**Coverage limit:** The minimal Docker build enables H.264 and AAC decoders for the valid control; other codecs can have null codec fields. AFL++ feedback is restricted to FFmpeg `mov.c` and uses one `/work/replay @@` process per input. Native in-process campaigns are unsupported for MLT's global plugin lifecycle.
