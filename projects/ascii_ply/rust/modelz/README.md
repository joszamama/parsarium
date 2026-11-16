# modelz — ASCII PLY / Rust

Pinned release: `0.1.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/rust/modelz/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply rust modelz
python3 parsarium.py run ascii_ply rust modelz controls/ascii_ply/triangle-unsigned-face.ply
python3 parsarium.py replay ascii_ply rust modelz CORPUS_DIR runs/ascii_ply-modelz-replay
python3 parsarium.py afl build ascii_ply rust modelz
python3 parsarium.py afl prepare ascii_ply rust modelz runs/ascii_ply-modelz-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
