# prx-wavefile — WAV / JavaScript

Pinned release: `11.0.0-prx.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/prx-wavefile/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript prx_wavefile
python3 parsarium.py run wav javascript prx_wavefile controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript prx_wavefile CORPUS_DIR runs/wav-prx_wavefile-replay
python3 parsarium.py afl build wav javascript prx_wavefile
python3 parsarium.py afl prepare wav javascript prx_wavefile runs/wav-prx_wavefile-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
