# dr_wav — WAV / C

Pinned release: `wav-0.14.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/c/dr-wav/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav c dr_wav
python3 parsarium.py run wav c dr_wav controls/wav/four-samples.wav
python3 parsarium.py replay wav c dr_wav CORPUS_DIR runs/wav-dr_wav-replay
python3 parsarium.py afl build wav c dr_wav
python3 parsarium.py afl prepare wav c dr_wav runs/wav-dr_wav-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
