# python-archive — ZIP / Python

Pinned release: `0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/python-archive/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python python_archive
python3 parsarium.py run zip python python_archive controls/zip/hello.zip
python3 parsarium.py replay zip python python_archive CORPUS_DIR runs/zip-python_archive-replay
python3 parsarium.py afl build zip python python_archive
python3 parsarium.py afl prepare zip python python_archive runs/zip-python_archive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
