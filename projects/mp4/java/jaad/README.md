# jaad — MP4 / Java

Pinned release: `0.8.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/java/jaad/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 java jaad
python3 parsarium.py run mp4 java jaad controls/mp4/red-av-no-udta.mp4
python3 parsarium.py replay mp4 java jaad CORPUS_DIR runs/mp4-jaad-replay
python3 parsarium.py afl build mp4 java jaad
python3 parsarium.py afl prepare mp4 java jaad runs/mp4-jaad-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
