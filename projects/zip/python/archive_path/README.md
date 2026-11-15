# archive-path — ZIP / Python

Pinned release: `0.4.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/archive-path/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python archive_path
python3 parsarium.py run zip python archive_path controls/zip/hello.zip
python3 parsarium.py replay zip python archive_path CORPUS_DIR runs/zip-archive_path-replay
python3 parsarium.py afl build zip python archive_path
python3 parsarium.py afl prepare zip python archive_path runs/zip-archive_path-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
