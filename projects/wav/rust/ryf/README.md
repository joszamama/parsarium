# ryf — WAV / Rust

Pinned release: `0.7.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/ryf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust ryf
python3 parsarium.py run wav rust ryf controls/wav/four-samples.wav
python3 parsarium.py replay wav rust ryf CORPUS_DIR runs/wav-ryf-replay
python3 parsarium.py afl build wav rust ryf
python3 parsarium.py afl prepare wav rust ryf runs/wav-ryf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
