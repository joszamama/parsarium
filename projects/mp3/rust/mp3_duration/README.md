# mp3-duration — MP3 / Rust

Pinned release: `0.1.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/rust/mp3-duration/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 rust mp3_duration
python3 parsarium.py run mp3 rust mp3_duration controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 rust mp3_duration CORPUS_DIR runs/mp3-mp3_duration-replay
python3 parsarium.py afl build mp3 rust mp3_duration
python3 parsarium.py afl prepare mp3 rust mp3_duration runs/mp3-mp3_duration-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
