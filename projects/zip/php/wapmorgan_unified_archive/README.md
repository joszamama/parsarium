# wapmorgan/unified-archive — ZIP / PHP

Pinned release: `1.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/wapmorgan-unified-archive/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php wapmorgan_unified_archive
python3 parsarium.py run zip php wapmorgan_unified_archive controls/zip/hello.zip
python3 parsarium.py replay zip php wapmorgan_unified_archive CORPUS_DIR runs/zip-wapmorgan_unified_archive-replay
python3 parsarium.py afl build zip php wapmorgan_unified_archive
python3 parsarium.py afl prepare zip php wapmorgan_unified_archive runs/zip-wapmorgan_unified_archive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
