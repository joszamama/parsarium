# symphonia — MP4 / Rust

Pinned release: `0.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/rust/symphonia/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 rust symphonia
python3 parsarium.py run mp4 rust symphonia controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 rust symphonia CORPUS_DIR runs/mp4-symphonia-replay
python3 parsarium.py afl build mp4 rust symphonia
python3 parsarium.py afl prepare mp4 rust symphonia runs/mp4-symphonia-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
