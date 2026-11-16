# lofty — MP4 / Rust

Pinned release: `0.25.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/rust/lofty/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 rust lofty
python3 parsarium.py run mp4 rust lofty controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 rust lofty CORPUS_DIR runs/mp4-lofty-replay
python3 parsarium.py afl build mp4 rust lofty
python3 parsarium.py afl prepare mp4 rust lofty runs/mp4-lofty-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
