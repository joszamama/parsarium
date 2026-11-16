# wav-codec — WAV / Rust

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/wav-codec/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust wav_codec
python3 parsarium.py run wav rust wav_codec controls/wav/four-samples.wav
python3 parsarium.py replay wav rust wav_codec CORPUS_DIR runs/wav-wav_codec-replay
python3 parsarium.py afl build wav rust wav_codec
python3 parsarium.py afl prepare wav rust wav_codec runs/wav-wav_codec-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
