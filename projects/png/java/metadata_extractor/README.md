# metadata-extractor — PNG / Java

Pinned release: `2.22.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/metadata-extractor/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java metadata_extractor
python3 parsarium.py run png java metadata_extractor controls/png/red-green.png
python3 parsarium.py replay png java metadata_extractor CORPUS_DIR runs/png-metadata_extractor-replay
python3 parsarium.py afl build png java metadata_extractor
python3 parsarium.py afl prepare png java metadata_extractor runs/png-metadata_extractor-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
