# archive/zip.OpenReader(path); File.Open() — ZIP / Go

Pinned release: `1.27.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/go/zip/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build zip go stdlib_openreader
python3 parsarium.py run zip go stdlib_openreader controls/zip/hello.zip
python3 parsarium.py replay zip go stdlib_openreader CORPUS_DIR runs/zip-stdlib_openreader-replay
python3 parsarium.py afl build zip go stdlib_openreader
python3 parsarium.py afl prepare zip go stdlib_openreader runs/zip-stdlib_openreader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
