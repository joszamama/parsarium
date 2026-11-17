# libheif — MP4 / C

Pinned release: `1.23.7`. [Manifest](manifest.json) · [Docker receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/mp4/c/libheif/verification.json)

[API, control result, and parser family](../../../../catalog/mp4/c/libheif/README.md)

libheif reads MP4 as an image sequence. It parses the `moov` and `trak` boxes and the visual sample entry. It skips the audio track, so the control reports one sequence track at 2×2. The harness accepts files up to 1 MiB with 1–64 parsed sequence tracks. The separate valid `red-av-3s.mp4` reports one 16×16 video track. This uses libheif's native ISO BMFF and sequence parser without a codec decoder.

The Docker control covered 1,684 pinned libheif source lines, including its ISO BMFF box reader, sequence-track parser, visual-track parser, and AVC box reader. The AFL++ overlay recorded 3,922 feedback edges on the control. A [fixed valid-variant check](../../../../fuzzing/afl-native/mp4/c/libheif/source-feedback.json) found a different map for `red-av-3s.mp4`. The prepared AFL command uses `@@` file input.

## Run from the repository root

```sh
python3 parsarium.py build mp4 c libheif
python3 parsarium.py run mp4 c libheif controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 c libheif CORPUS_DIR runs/mp4-libheif-replay
python3 parsarium.py afl build mp4 c libheif
python3 parsarium.py afl prepare mp4 c libheif runs/mp4-libheif-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
