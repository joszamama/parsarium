# miniz — ZIP / C

Pinned release: `3.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/c/miniz/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip c miniz
python3 parsarium.py run zip c miniz controls/zip/hello.zip
python3 parsarium.py replay zip c miniz CORPUS_DIR runs/zip-miniz-replay
python3 parsarium.py afl build zip c miniz
python3 parsarium.py afl prepare zip c miniz runs/zip-miniz-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
