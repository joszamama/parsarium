# riff-wave — WAV / Rust

Pinned release: `0.1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/riff-wave/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust riff_wave
python3 parsarium.py run wav rust riff_wave controls/wav/four-samples.wav
python3 parsarium.py replay wav rust riff_wave CORPUS_DIR runs/wav-riff_wave-replay
python3 parsarium.py afl build wav rust riff_wave
python3 parsarium.py afl prepare wav rust riff_wave runs/wav-riff_wave-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
