# mp4ameta — MP4 / Rust

Pinned release: `0.13.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/rust/mp4ameta/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 rust mp4ameta
python3 parsarium.py run mp4 rust mp4ameta controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 rust mp4ameta CORPUS_DIR runs/mp4-mp4ameta-replay
python3 parsarium.py afl build mp4 rust mp4ameta
python3 parsarium.py afl prepare mp4 rust mp4ameta runs/mp4-mp4ameta-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
