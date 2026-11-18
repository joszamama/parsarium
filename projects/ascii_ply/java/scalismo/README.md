# scalismo_3 — ASCII PLY / Java

Pinned release: `1.0-RC1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/java/scalismo-3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply java scalismo
python3 parsarium.py run ascii_ply java scalismo controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply java scalismo CORPUS_DIR runs/ascii_ply-scalismo-replay
python3 parsarium.py afl build ascii_ply java scalismo
python3 parsarium.py afl prepare ascii_ply java scalismo runs/ascii_ply-scalismo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
