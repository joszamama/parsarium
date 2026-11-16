# wuffs — PNG / C++

Pinned release: `0.3.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/cpp/wuffs/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png cpp wuffs
python3 parsarium.py run png cpp wuffs controls/png/red-green.png
python3 parsarium.py replay png cpp wuffs CORPUS_DIR runs/png-wuffs-replay
python3 parsarium.py afl build png cpp wuffs
python3 parsarium.py afl prepare png cpp wuffs runs/png-wuffs-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
