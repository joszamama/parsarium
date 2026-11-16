# wav-file-decoder — WAV / JavaScript

Pinned release: `1.0.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/javascript/wav-file-decoder/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav javascript wav_file_decoder
python3 parsarium.py run wav javascript wav_file_decoder controls/wav/four-samples.wav
python3 parsarium.py replay wav javascript wav_file_decoder CORPUS_DIR runs/wav-wav_file_decoder-replay
python3 parsarium.py afl build wav javascript wav_file_decoder
python3 parsarium.py afl prepare wav javascript wav_file_decoder runs/wav-wav_file_decoder-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
