# taglib — WAV / C

Pinned release: `2.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/c/taglib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav c taglib
python3 parsarium.py run wav c taglib controls/wav/four-samples.wav
python3 parsarium.py replay wav c taglib CORPUS_DIR runs/wav-taglib-replay
python3 parsarium.py afl build wav c taglib
python3 parsarium.py afl prepare wav c taglib runs/wav-taglib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
