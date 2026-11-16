# libpointmatcher — ASCII PLY / C++

Pinned release: `1.4.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/cpp/libpointmatcher/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply cpp libpointmatcher
python3 parsarium.py run ascii_ply cpp libpointmatcher controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply cpp libpointmatcher CORPUS_DIR runs/ascii_ply-libpointmatcher-replay
python3 parsarium.py afl build ascii_ply cpp libpointmatcher
python3 parsarium.py afl prepare ascii_ply cpp libpointmatcher runs/ascii_ply-libpointmatcher-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
