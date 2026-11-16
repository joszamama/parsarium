# wav-reader-ts — WAV / JavaScript

Pinned release: `1.0.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/wav-reader-ts/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript wav_reader_ts
python3 parsarium.py run wav javascript wav_reader_ts controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript wav_reader_ts CORPUS_DIR runs/wav-wav_reader_ts-replay
python3 parsarium.py afl build wav javascript wav_reader_ts
python3 parsarium.py afl prepare wav javascript wav_reader_ts runs/wav-wav_reader_ts-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
