# rasuvaeff/media-converter — WAV / PHP

Pinned release: `v1.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/rasuvaeff-media-converter/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php rasuvaeff_media_converter
python3 parsarium.py run wav php rasuvaeff_media_converter controls/wav/256-samples.wav
python3 parsarium.py replay wav php rasuvaeff_media_converter CORPUS_DIR runs/wav-rasuvaeff_media_converter-replay
python3 parsarium.py afl build wav php rasuvaeff_media_converter
python3 parsarium.py afl prepare wav php rasuvaeff_media_converter runs/wav-rasuvaeff_media_converter-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
