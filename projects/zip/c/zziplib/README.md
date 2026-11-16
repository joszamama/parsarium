# zziplib — ZIP / C

Pinned release: `0.13.80`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/zip/c/zziplib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build zip c zziplib
python3 parsarium.py run zip c zziplib controls/zip/hello.zip
python3 parsarium.py replay zip c zziplib CORPUS_DIR runs/zip-zziplib-replay
python3 parsarium.py afl build zip c zziplib
python3 parsarium.py afl prepare zip c zziplib runs/zip-zziplib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
