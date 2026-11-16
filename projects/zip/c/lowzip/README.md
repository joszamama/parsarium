# lowzip — ZIP / C

Pinned release: `1.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/c/lowzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip c lowzip
python3 parsarium.py run zip c lowzip controls/zip/hello.zip
python3 parsarium.py replay zip c lowzip CORPUS_DIR runs/zip-lowzip-replay
python3 parsarium.py afl build zip c lowzip
python3 parsarium.py afl prepare zip c lowzip runs/zip-lowzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
