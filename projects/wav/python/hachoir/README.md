# hachoir — WAV / Python

Pinned release: `3.4.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/hachoir/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python hachoir
python3 parsarium.py run wav python hachoir controls/wav/four-samples.wav
python3 parsarium.py replay wav python hachoir CORPUS_DIR runs/wav-hachoir-replay
python3 parsarium.py afl build wav python hachoir
python3 parsarium.py afl prepare wav python hachoir runs/wav-hachoir-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
