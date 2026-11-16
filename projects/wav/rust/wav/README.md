# wav — WAV / Rust

Pinned release: `1.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/wav/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust wav
python3 parsarium.py run wav rust wav controls/wav/four-samples.wav
python3 parsarium.py replay wav rust wav CORPUS_DIR runs/wav-wav-replay
python3 parsarium.py afl build wav rust wav
python3 parsarium.py afl prepare wav rust wav runs/wav-wav-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
