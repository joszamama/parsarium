# metadata-extractor — MP4 / Java

Pinned release: `2.22.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/java/metadata-extractor/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 java metadata_extractor
python3 parsarium.py run mp4 java metadata_extractor controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 java metadata_extractor CORPUS_DIR runs/mp4-metadata_extractor-replay
python3 parsarium.py afl build mp4 java metadata_extractor
python3 parsarium.py afl prepare mp4 java metadata_extractor runs/mp4-metadata_extractor-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
