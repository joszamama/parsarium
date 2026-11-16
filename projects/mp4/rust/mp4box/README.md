# mp4box — MP4 / Rust

Pinned release: `0.14.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/rust/mp4box/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 rust mp4box
python3 parsarium.py run mp4 rust mp4box controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 rust mp4box CORPUS_DIR runs/mp4-mp4box-replay
python3 parsarium.py afl build mp4 rust mp4box
python3 parsarium.py afl prepare mp4 rust mp4box runs/mp4-mp4box-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
