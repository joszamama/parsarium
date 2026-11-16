# zziplib — ZIP / C++

Pinned release: `0.13.80`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/cpp/zziplib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip cpp zziplib
python3 parsarium.py run zip cpp zziplib controls/zip/hello.zip
python3 parsarium.py replay zip cpp zziplib CORPUS_DIR runs/zip-zziplib-replay
python3 parsarium.py afl build zip cpp zziplib
python3 parsarium.py afl prepare zip cpp zziplib runs/zip-zziplib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
