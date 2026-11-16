# metadata-extractor — WAV / Java

Pinned release: `2.19.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/metadata-extractor/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java metadata_extractor
python3 parsarium.py run wav java metadata_extractor controls/wav/256-samples.wav
python3 parsarium.py replay wav java metadata_extractor CORPUS_DIR runs/wav-metadata_extractor-replay
python3 parsarium.py afl build wav java metadata_extractor
python3 parsarium.py afl prepare wav java metadata_extractor runs/wav-metadata_extractor-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
