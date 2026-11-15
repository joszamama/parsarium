# zipmonkey — ZIP / Python

Pinned release: `1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/zipmonkey/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python zipmonkey
python3 parsarium.py run zip python zipmonkey controls/zip/hello.zip
python3 parsarium.py replay zip python zipmonkey CORPUS_DIR runs/zip-zipmonkey-replay
python3 parsarium.py afl build zip python zipmonkey
python3 parsarium.py afl prepare zip python zipmonkey runs/zip-zipmonkey-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
