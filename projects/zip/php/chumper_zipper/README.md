# chumper/zipper — ZIP / PHP

Pinned release: `v1.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/chumper-zipper/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php chumper_zipper
python3 parsarium.py run zip php chumper_zipper controls/zip/hello.zip
python3 parsarium.py replay zip php chumper_zipper CORPUS_DIR runs/zip-chumper_zipper-replay
python3 parsarium.py afl build zip php chumper_zipper
python3 parsarium.py afl prepare zip php chumper_zipper runs/zip-chumper_zipper-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
