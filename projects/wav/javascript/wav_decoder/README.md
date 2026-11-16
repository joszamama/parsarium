# wav-decoder — WAV / JavaScript

Pinned release: `1.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/wav-decoder/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript wav_decoder
python3 parsarium.py run wav javascript wav_decoder controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript wav_decoder CORPUS_DIR runs/wav-wav_decoder-replay
python3 parsarium.py afl build wav javascript wav_decoder
python3 parsarium.py afl prepare wav javascript wav_decoder runs/wav-wav_decoder-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
