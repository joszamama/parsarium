# libheif — MP4 / C++

Pinned release: `1.23.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/cpp/libheif/README.md)

libheif reads MP4 as an image sequence. The C++17 harness calls the libheif C API through RAII wrappers. It parses the `moov` and `trak` boxes and the visual sample entry. It skips the audio track, so the control reports one sequence track at 2×2. The harness accepts files with 1–16 parsed sequence tracks. This uses libheif's native ISO BMFF and sequence parser without a codec decoder.

The exact control covers 1,684 libheif source lines, including 284 sequence-box parser lines. AFL++ reports 3,943 edges. A second valid MP4 reports a 16×16 video track and changes 188 edge IDs.

## Run from the repository root

```sh
python3 parsarium.py build mp4 cpp libheif
python3 parsarium.py run mp4 cpp libheif controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 cpp libheif CORPUS_DIR runs/mp4-libheif-cpp-replay
python3 parsarium.py afl build mp4 cpp libheif
python3 parsarium.py afl prepare mp4 cpp libheif runs/mp4-libheif-cpp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
