# ferrum_cloud — ASCII PLY / Rust

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/rust/ferrum-cloud/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply rust ferrum_cloud
python3 parsarium.py run ascii_ply rust ferrum_cloud controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply rust ferrum_cloud CORPUS_DIR runs/ascii_ply-ferrum_cloud-replay
python3 parsarium.py afl build ascii_ply rust ferrum_cloud
python3 parsarium.py afl prepare ascii_ply rust ferrum_cloud runs/ascii_ply-ferrum_cloud-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
