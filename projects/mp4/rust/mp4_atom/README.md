# mp4-atom — MP4 / Rust

Pinned release: `0.17.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/rust/mp4-atom/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 rust mp4_atom
python3 parsarium.py run mp4 rust mp4_atom controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 rust mp4_atom CORPUS_DIR runs/mp4-mp4_atom-replay
python3 parsarium.py afl build mp4 rust mp4_atom
python3 parsarium.py afl prepare mp4 rust mp4_atom runs/mp4-mp4_atom-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
