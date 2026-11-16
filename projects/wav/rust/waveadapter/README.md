# waveadapter — WAV / Rust

Pinned release: `0.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/waveadapter/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust waveadapter
python3 parsarium.py run wav rust waveadapter controls/wav/four-samples.wav
python3 parsarium.py replay wav rust waveadapter CORPUS_DIR runs/wav-waveadapter-replay
python3 parsarium.py afl build wav rust waveadapter
python3 parsarium.py afl prepare wav rust waveadapter runs/wav-waveadapter-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
