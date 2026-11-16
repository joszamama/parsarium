# omni-archive — ZIP / Python

Pinned release: `0.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/python/omni-archive/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip python omni_archive
python3 parsarium.py run zip python omni_archive controls/zip/hello.zip
python3 parsarium.py replay zip python omni_archive CORPUS_DIR runs/zip-omni_archive-replay
python3 parsarium.py afl build zip python omni_archive
python3 parsarium.py afl prepare zip python omni_archive runs/zip-omni_archive-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
