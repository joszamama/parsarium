# revelo-parsers-container — MP4 / Rust

Pinned release: `0.5.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/rust/revelo-parsers-container/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 rust revelo_parsers_container
python3 parsarium.py run mp4 rust revelo_parsers_container controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 rust revelo_parsers_container CORPUS_DIR runs/mp4-revelo_parsers_container-replay
python3 parsarium.py afl build mp4 rust revelo_parsers_container
python3 parsarium.py afl prepare mp4 rust revelo_parsers_container runs/mp4-revelo_parsers_container-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
