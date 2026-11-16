# audio-file — WAV / Rust

Pinned release: `0.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/rust/audio-file/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav rust audio_file
python3 parsarium.py run wav rust audio_file controls/wav/four-samples.wav
python3 parsarium.py replay wav rust audio_file CORPUS_DIR runs/wav-audio_file-replay
python3 parsarium.py afl build wav rust audio_file
python3 parsarium.py afl prepare wav rust audio_file runs/wav-audio_file-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
