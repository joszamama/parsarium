# bwavfile — WAV / Rust

Pinned release: `2.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/bwavfile/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust bwavfile
python3 parsarium.py run wav rust bwavfile controls/wav/four-samples.wav
python3 parsarium.py replay wav rust bwavfile CORPUS_DIR runs/wav-bwavfile-replay
python3 parsarium.py afl build wav rust bwavfile
python3 parsarium.py afl prepare wav rust bwavfile runs/wav-bwavfile-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
