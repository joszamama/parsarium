# old-isoparser — MP4 / Java

Pinned release: `1.1.22`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/java/old-isoparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 java old_isoparser
python3 parsarium.py run mp4 java old_isoparser controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 java old_isoparser CORPUS_DIR runs/mp4-old_isoparser-replay
python3 parsarium.py afl build mp4 java old_isoparser
python3 parsarium.py afl prepare mp4 java old_isoparser runs/mp4-old_isoparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
