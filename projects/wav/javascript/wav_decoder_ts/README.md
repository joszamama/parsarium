# wav-decoder-ts — WAV / JavaScript

Pinned release: `1.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/wav-decoder-ts/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript wav_decoder_ts
python3 parsarium.py run wav javascript wav_decoder_ts controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript wav_decoder_ts CORPUS_DIR runs/wav-wav_decoder_ts-replay
python3 parsarium.py afl build wav javascript wav_decoder_ts
python3 parsarium.py afl prepare wav javascript wav_decoder_ts runs/wav-wav_decoder_ts-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
