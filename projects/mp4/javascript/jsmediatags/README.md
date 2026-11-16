# jsmediatags — MP4 / JavaScript

Pinned release: `3.9.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/javascript/jsmediatags/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 javascript jsmediatags
python3 parsarium.py run mp4 javascript jsmediatags controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 javascript jsmediatags CORPUS_DIR runs/mp4-jsmediatags-replay
python3 parsarium.py afl build mp4 javascript jsmediatags
python3 parsarium.py afl prepare mp4 javascript jsmediatags runs/mp4-jsmediatags-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
