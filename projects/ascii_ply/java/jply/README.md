# jply — ASCII PLY / Java

Pinned release: `0.2.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/java/jply/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply java jply
python3 parsarium.py run ascii_ply java jply controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply java jply CORPUS_DIR runs/ascii_ply-jply-replay
python3 parsarium.py afl build ascii_ply java jply
python3 parsarium.py afl prepare ascii_ply java jply runs/ascii_ply-jply-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
