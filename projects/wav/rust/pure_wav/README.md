# pure_wav — WAV / Rust

Pinned release: `2.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/pure-wav/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust pure_wav
python3 parsarium.py run wav rust pure_wav controls/wav/four-samples.wav
python3 parsarium.py replay wav rust pure_wav CORPUS_DIR runs/wav-pure_wav-replay
python3 parsarium.py afl build wav rust pure_wav
python3 parsarium.py afl prepare wav rust pure_wav runs/wav-pure_wav-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
