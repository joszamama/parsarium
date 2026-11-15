# taglib — MP4 / C++

Pinned release: `2.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/cpp/taglib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 cpp taglib
python3 parsarium.py run mp4 cpp taglib controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 cpp taglib CORPUS_DIR runs/mp4-taglib-replay
python3 parsarium.py afl build mp4 cpp taglib
python3 parsarium.py afl prepare mp4 cpp taglib runs/mp4-taglib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
