# wave_stream — WAV / Rust

Pinned release: `0.6.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/wave-stream/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust wave_stream
python3 parsarium.py run wav rust wave_stream controls/wav/four-samples.wav
python3 parsarium.py replay wav rust wave_stream CORPUS_DIR runs/wav-wave_stream-replay
python3 parsarium.py afl build wav rust wave_stream
python3 parsarium.py afl prepare wav rust wave_stream runs/wav-wave_stream-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
