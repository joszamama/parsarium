# simpleaudio — WAV / Python

Pinned release: `1.0.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/python/simpleaudio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav python simpleaudio
python3 parsarium.py run wav python simpleaudio controls/wav/four-samples.wav
python3 parsarium.py replay wav python simpleaudio CORPUS_DIR runs/wav-simpleaudio-replay
python3 parsarium.py afl build wav python simpleaudio
python3 parsarium.py afl prepare wav python simpleaudio runs/wav-simpleaudio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
