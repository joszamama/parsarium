# nanomp3 — MP3 / Rust

Pinned release: `0.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/rust/nanomp3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3_id3v2 rust nanomp3
python3 parsarium.py run mp3_id3v2 rust nanomp3 controls/mp3_id3v2/tone-tags.mp3
python3 parsarium.py replay mp3_id3v2 rust nanomp3 CORPUS_DIR runs/mp3_id3v2-nanomp3-replay
python3 parsarium.py afl build mp3_id3v2 rust nanomp3
python3 parsarium.py afl prepare mp3_id3v2 rust nanomp3 runs/mp3_id3v2-nanomp3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
