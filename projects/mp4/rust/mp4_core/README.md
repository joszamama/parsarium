# mp4-core — MP4 / Rust

Pinned release: `0.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/rust/mp4-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 rust mp4_core
python3 parsarium.py run mp4 rust mp4_core controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 rust mp4_core CORPUS_DIR runs/mp4-mp4_core-replay
python3 parsarium.py afl build mp4 rust mp4_core
python3 parsarium.py afl prepare mp4 rust mp4_core runs/mp4-mp4_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
