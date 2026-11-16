# zipfile-zstd — ZIP / Python

Pinned release: `0.0.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/zipfile-zstd/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python zipfile_zstd
python3 parsarium.py run zip python zipfile_zstd controls/zip/hello-zstd.zip
python3 parsarium.py replay zip python zipfile_zstd CORPUS_DIR runs/zip-zipfile_zstd-replay
python3 parsarium.py afl build zip python zipfile_zstd
python3 parsarium.py afl prepare zip python zipfile_zstd runs/zip-zipfile_zstd-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
