# symphonia — WAV / Rust

Pinned release: `0.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/symphonia/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust symphonia
python3 parsarium.py run wav rust symphonia controls/wav/four-samples.wav
python3 parsarium.py replay wav rust symphonia CORPUS_DIR runs/wav-symphonia-replay
python3 parsarium.py afl build wav rust symphonia
python3 parsarium.py afl prepare wav rust symphonia runs/wav-symphonia-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
