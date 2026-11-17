# nanomp3 — MP3 / Rust

Pinned release: `0.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp3/rust/nanomp3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp3 rust nanomp3
python3 parsarium.py run mp3 rust nanomp3 controls/mp3/tone-44k-mono.mp3
python3 parsarium.py replay mp3 rust nanomp3 CORPUS_DIR runs/mp3-nanomp3-replay
python3 parsarium.py afl build mp3 rust nanomp3
python3 parsarium.py afl prepare mp3 rust nanomp3 runs/mp3-nanomp3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Pure-Rust port of the minimp3 decoder: same parser family as the selected minimp3 binding, not an independent engine. Untagged CBR MPEG Layer III controls only; no VBR, Xing/Info, tags, free-format, Layer I/II, MPEG-2.5 or malformed input tested.
