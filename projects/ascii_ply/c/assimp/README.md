# assimp — ASCII PLY / C

Pinned release: `6.0.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/c/assimp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply c assimp
python3 parsarium.py run ascii_ply c assimp controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply c assimp CORPUS_DIR runs/ascii_ply-assimp-replay
python3 parsarium.py afl build ascii_ply c assimp
python3 parsarium.py afl prepare ascii_ply c assimp runs/ascii_ply-assimp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
