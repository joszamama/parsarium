# nwav — WAV / Rust

Pinned release: `0.1.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/nwav/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust nwav
python3 parsarium.py run wav rust nwav controls/wav/four-samples.wav
python3 parsarium.py replay wav rust nwav CORPUS_DIR runs/wav-nwav-replay
python3 parsarium.py afl build wav rust nwav
python3 parsarium.py afl prepare wav rust nwav runs/wav-nwav-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
