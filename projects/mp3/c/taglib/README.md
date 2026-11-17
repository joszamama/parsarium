# taglib — MP3 / C

Pinned release: `2.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/c/taglib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 c taglib
python3 parsarium.py run mp3 c taglib controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 c taglib CORPUS_DIR runs/mp3-taglib-replay
python3 parsarium.py afl build mp3 c taglib
python3 parsarium.py afl prepare mp3 c taglib runs/mp3-taglib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
