# mp4parse-patched — MP4 / Rust

Pinned release: `0.17.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/rust/mp4parse-patched/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 rust mp4parse_patched
python3 parsarium.py run mp4 rust mp4parse_patched controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 rust mp4parse_patched CORPUS_DIR runs/mp4-mp4parse_patched-replay
python3 parsarium.py afl build mp4 rust mp4parse_patched
python3 parsarium.py afl prepare mp4 rust mp4parse_patched runs/mp4-mp4parse_patched-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
