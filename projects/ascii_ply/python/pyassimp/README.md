# pyassimp — ASCII PLY / Python

Pinned release: `5.2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/python/pyassimp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply python pyassimp
python3 parsarium.py run ascii_ply python pyassimp controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply python pyassimp CORPUS_DIR runs/ascii_ply-pyassimp-replay
python3 parsarium.py afl build ascii_ply python pyassimp
python3 parsarium.py afl prepare ascii_ply python pyassimp runs/ascii_ply-pyassimp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
