# tallison-isoparser — MP4 / Java

Pinned release: `1.9.41.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/java/tallison-isoparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 java tallison_isoparser
python3 parsarium.py run mp4 java tallison_isoparser controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 java tallison_isoparser CORPUS_DIR runs/mp4-tallison_isoparser-replay
python3 parsarium.py afl build mp4 java tallison_isoparser
python3 parsarium.py afl prepare mp4 java tallison_isoparser runs/mp4-tallison_isoparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
