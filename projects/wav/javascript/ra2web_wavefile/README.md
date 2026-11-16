# @ra2web/wavefile — WAV / JavaScript

Pinned release: `1.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/ra2web-wavefile/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript ra2web_wavefile
python3 parsarium.py run wav javascript ra2web_wavefile controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript ra2web_wavefile CORPUS_DIR runs/wav-ra2web_wavefile-replay
python3 parsarium.py afl build wav javascript ra2web_wavefile
python3 parsarium.py afl prepare wav javascript ra2web_wavefile runs/wav-ra2web_wavefile-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
