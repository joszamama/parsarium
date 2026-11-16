# wavers — WAV / Rust

Pinned release: `1.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/wavers/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust wavers
python3 parsarium.py run wav rust wavers controls/wav/four-samples.wav
python3 parsarium.py replay wav rust wavers CORPUS_DIR runs/wav-wavers-replay
python3 parsarium.py afl build wav rust wavers
python3 parsarium.py afl prepare wav rust wavers runs/wav-wavers-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
