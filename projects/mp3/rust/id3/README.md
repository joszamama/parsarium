# id3 — MP3 / Rust

Pinned release: `1.17.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/rust/id3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 rust id3
python3 parsarium.py run mp3 rust id3 controls/mp3/id3v2-tagged-tone.mp3
python3 parsarium.py replay mp3 rust id3 CORPUS_DIR runs/mp3-id3-replay
python3 parsarium.py afl build mp3 rust id3
python3 parsarium.py afl prepare mp3 rust id3 runs/mp3-id3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
