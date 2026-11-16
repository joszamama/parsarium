# madnest/madzipper — ZIP / PHP

Pinned release: `1.6.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/php/madnest-madzipper/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip php madnest_madzipper
python3 parsarium.py run zip php madnest_madzipper controls/zip/hello.zip
python3 parsarium.py replay zip php madnest_madzipper CORPUS_DIR runs/zip-madnest_madzipper-replay
python3 parsarium.py afl build zip php madnest_madzipper
python3 parsarium.py afl prepare zip php madnest_madzipper runs/zip-madnest_madzipper-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
