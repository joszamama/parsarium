# surge-hound — WAV / Rust

Pinned release: `0.2.11-alpha.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/surge-hound/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust surge_hound
python3 parsarium.py run wav rust surge_hound controls/wav/four-samples.wav
python3 parsarium.py replay wav rust surge_hound CORPUS_DIR runs/wav-surge_hound-replay
python3 parsarium.py afl build wav rust surge_hound
python3 parsarium.py afl prepare wav rust surge_hound runs/wav-surge_hound-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
