# symphonium — WAV / Rust

Pinned release: `0.13.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/symphonium/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust symphonium
python3 parsarium.py run wav rust symphonium controls/wav/four-samples.wav
python3 parsarium.py replay wav rust symphonium CORPUS_DIR runs/wav-symphonium-replay
python3 parsarium.py afl build wav rust symphonium
python3 parsarium.py afl prepare wav rust symphonium runs/wav-symphonium-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
