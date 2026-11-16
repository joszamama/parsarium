# aubio — WAV / C

Pinned release: `0.4.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/c/aubio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav c aubio
python3 parsarium.py run wav c aubio controls/wav/four-samples.wav
python3 parsarium.py replay wav c aubio CORPUS_DIR runs/wav-aubio-replay
python3 parsarium.py afl build wav c aubio
python3 parsarium.py afl prepare wav c aubio runs/wav-aubio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
