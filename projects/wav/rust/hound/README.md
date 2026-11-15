# hound — WAV / Rust

Pinned release: `3.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/hound/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust hound
python3 parsarium.py run wav rust hound controls/wav/four-samples.wav
python3 parsarium.py replay wav rust hound CORPUS_DIR runs/wav-hound-replay
python3 parsarium.py afl build wav rust hound
python3 parsarium.py afl prepare wav rust hound runs/wav-hound-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
