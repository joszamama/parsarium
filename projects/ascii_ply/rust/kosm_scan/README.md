# kosm-scan — ASCII PLY / Rust

Pinned release: `0.0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/rust/kosm-scan/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply rust kosm_scan
python3 parsarium.py run ascii_ply rust kosm_scan controls/ascii_ply/triangle-colour.ply
python3 parsarium.py replay ascii_ply rust kosm_scan CORPUS_DIR runs/ascii_ply-kosm_scan-replay
python3 parsarium.py afl build ascii_ply rust kosm_scan
python3 parsarium.py afl prepare ascii_ply rust kosm_scan runs/ascii_ply-kosm_scan-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
