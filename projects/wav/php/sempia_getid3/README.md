# sempia/getid3 — WAV / PHP

Pinned release: `2.0.0.0-p1.9.25`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/sempia-getid3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php sempia_getid3
python3 parsarium.py run wav php sempia_getid3 controls/wav/256-samples.wav
python3 parsarium.py replay wav php sempia_getid3 CORPUS_DIR runs/wav-sempia_getid3-replay
python3 parsarium.py afl build wav php sempia_getid3
python3 parsarium.py afl prepare wav php sempia_getid3 runs/wav-sempia_getid3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
