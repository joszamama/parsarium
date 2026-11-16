# mp4-box-encoding — MP4 / JavaScript

Pinned release: `1.4.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/javascript/mp4-box-encoding/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 javascript mp4_box_encoding
python3 parsarium.py run mp4 javascript mp4_box_encoding controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 javascript mp4_box_encoding CORPUS_DIR runs/mp4-mp4_box_encoding-replay
python3 parsarium.py afl build mp4 javascript mp4_box_encoding
python3 parsarium.py afl prepare mp4 javascript mp4_box_encoding runs/mp4-mp4_box_encoding-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
