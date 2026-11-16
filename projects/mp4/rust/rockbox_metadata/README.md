# rockbox-metadata — MP4 / Rust

Pinned release: `0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/rust/rockbox-metadata/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 rust rockbox_metadata
python3 parsarium.py run mp4 rust rockbox_metadata controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 rust rockbox_metadata CORPUS_DIR runs/mp4-rockbox_metadata-replay
python3 parsarium.py afl build mp4 rust rockbox_metadata
python3 parsarium.py afl prepare mp4 rust rockbox_metadata runs/mp4-rockbox_metadata-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
