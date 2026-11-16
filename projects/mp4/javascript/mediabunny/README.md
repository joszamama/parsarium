# mediabunny — MP4 / JavaScript

Pinned release: `1.65.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/javascript/mediabunny/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 javascript mediabunny
python3 parsarium.py run mp4 javascript mediabunny controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 javascript mediabunny CORPUS_DIR runs/mp4-mediabunny-replay
python3 parsarium.py afl build mp4 javascript mediabunny
python3 parsarium.py afl prepare mp4 javascript mediabunny runs/mp4-mediabunny-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
