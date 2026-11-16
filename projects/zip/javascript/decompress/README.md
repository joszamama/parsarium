# decompress — ZIP / JavaScript

Pinned release: `4.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/javascript/decompress/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip javascript decompress
python3 parsarium.py run zip javascript decompress controls/zip/hello.zip
python3 parsarium.py replay zip javascript decompress CORPUS_DIR runs/zip-decompress-replay
python3 parsarium.py afl build zip javascript decompress
python3 parsarium.py afl prepare zip javascript decompress runs/zip-decompress-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
