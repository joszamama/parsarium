# geogram — ASCII PLY / C++

Pinned release: `1.10.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/cpp/geogram/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply cpp geogram
python3 parsarium.py run ascii_ply cpp geogram controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply cpp geogram CORPUS_DIR runs/ascii_ply-geogram-replay
python3 parsarium.py afl build ascii_ply cpp geogram
python3 parsarium.py afl prepare ascii_ply cpp geogram runs/ascii_ply-geogram-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
