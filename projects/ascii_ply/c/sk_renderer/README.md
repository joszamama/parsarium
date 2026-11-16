# sk_renderer — ASCII PLY / C

Pinned release: `v2026.11.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/c/sk-renderer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply c sk_renderer
python3 parsarium.py run ascii_ply c sk_renderer controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply c sk_renderer CORPUS_DIR runs/ascii_ply-sk_renderer-replay
python3 parsarium.py afl build ascii_ply c sk_renderer
python3 parsarium.py afl prepare ascii_ply c sk_renderer runs/ascii_ply-sk_renderer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
