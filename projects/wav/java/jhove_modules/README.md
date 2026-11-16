# jhove-modules — WAV / Java

Pinned release: `1.20.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/jhove-modules/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java jhove_modules
python3 parsarium.py run wav java jhove_modules controls/wav/256-samples.wav
python3 parsarium.py replay wav java jhove_modules CORPUS_DIR runs/wav-jhove_modules-replay
python3 parsarium.py afl build wav java jhove_modules
python3 parsarium.py afl prepare wav java jhove_modules runs/wav-jhove_modules-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
