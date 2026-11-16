# brlcad — ASCII PLY / C

Pinned release: `7.46.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/c/brlcad/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply c brlcad
python3 parsarium.py run ascii_ply c brlcad controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply c brlcad CORPUS_DIR runs/ascii_ply-brlcad-replay
python3 parsarium.py afl build ascii_ply c brlcad
python3 parsarium.py afl prepare ascii_ply c brlcad runs/ascii_ply-brlcad-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run. [Reason](inprocess-blocker.json).
