# stream-unzip — ZIP / Python

Pinned release: `0.0.101`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/stream-unzip/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python stream_unzip
python3 parsarium.py run zip python stream_unzip controls/zip/hello.zip
python3 parsarium.py replay zip python stream_unzip CORPUS_DIR runs/zip-stream_unzip-replay
python3 parsarium.py afl build zip python stream_unzip
python3 parsarium.py afl prepare zip python stream_unzip runs/zip-stream_unzip-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
