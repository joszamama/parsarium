# wave — WAV / Python

Pinned release: `3.13.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/python/wav/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build wav python stdlib_wave
python3 parsarium.py run wav python stdlib_wave controls/wav/four-samples.wav
python3 parsarium.py replay wav python stdlib_wave CORPUS_DIR runs/wav-stdlib_wave-replay
python3 parsarium.py afl build wav python stdlib_wave
python3 parsarium.py afl prepare wav python stdlib_wave runs/wav-stdlib_wave-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
