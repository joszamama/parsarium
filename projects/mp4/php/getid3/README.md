# james-heinrich/getid3 — MP4 / PHP

Pinned release: `v1.9.28`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/james-heinrich-getid3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php getid3
python3 parsarium.py run mp4 php getid3 controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php getid3 CORPUS_DIR runs/mp4-getid3-replay
python3 parsarium.py afl build mp4 php getid3
python3 parsarium.py afl prepare mp4 php getid3 runs/mp4-getid3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
