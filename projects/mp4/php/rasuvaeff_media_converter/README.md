# rasuvaeff/media-converter — MP4 / PHP

Pinned release: `v1.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/rasuvaeff-media-converter/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php rasuvaeff_media_converter
python3 parsarium.py run mp4 php rasuvaeff_media_converter controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php rasuvaeff_media_converter CORPUS_DIR runs/mp4-rasuvaeff_media_converter-replay
python3 parsarium.py afl build mp4 php rasuvaeff_media_converter
python3 parsarium.py afl prepare mp4 php rasuvaeff_media_converter runs/mp4-rasuvaeff_media_converter-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
