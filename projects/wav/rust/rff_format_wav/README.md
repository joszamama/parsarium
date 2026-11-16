# rff-format-wav — WAV / Rust

Pinned release: `0.4.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/rff-format-wav/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust rff_format_wav
python3 parsarium.py run wav rust rff_format_wav controls/wav/four-samples.wav
python3 parsarium.py replay wav rust rff_format_wav CORPUS_DIR runs/wav-rff_format_wav-replay
python3 parsarium.py afl build wav rust rff_format_wav
python3 parsarium.py afl prepare wav rust rff_format_wav runs/wav-rff_format_wav-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
