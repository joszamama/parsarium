# lwjgl-assimp — ASCII PLY / Java

Pinned release: `3.4.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/java/lwjgl-assimp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply java lwjgl_assimp
python3 parsarium.py run ascii_ply java lwjgl_assimp controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply java lwjgl_assimp CORPUS_DIR runs/ascii_ply-lwjgl_assimp-replay
python3 parsarium.py afl build ascii_ply java lwjgl_assimp
python3 parsarium.py afl prepare ascii_ply java lwjgl_assimp runs/ascii_ply-lwjgl_assimp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
