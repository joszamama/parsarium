# mp4tree — MP4 / JavaScript

Pinned release: `0.10.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/javascript/mp4tree/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 javascript mp4tree
python3 parsarium.py run mp4 javascript mp4tree controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 javascript mp4tree CORPUS_DIR runs/mp4-mp4tree-replay
python3 parsarium.py afl build mp4 javascript mp4tree
python3 parsarium.py afl prepare mp4 javascript mp4tree runs/mp4-mp4tree-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
