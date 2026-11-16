# wav_io — WAV / Rust

Pinned release: `0.1.17`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/wav-io/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust wav_io
python3 parsarium.py run wav rust wav_io controls/wav/four-samples.wav
python3 parsarium.py replay wav rust wav_io CORPUS_DIR runs/wav-wav_io-replay
python3 parsarium.py afl build wav rust wav_io
python3 parsarium.py afl prepare wav rust wav_io runs/wav-wav_io-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
