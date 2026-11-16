# brlcad — ASCII PLY / C

Pinned release: `7.46.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_ply/c/brlcad/README.md)

The GCV PLY plugin uses bundled RPly 1.1.4 for syntax parsing. The harness reports the imported BRL-CAD BOT mesh and the plugin's default 1000× coordinate scale.

Each input runs in a fresh process. BRL-CAD 7.46.0's PLY vertex callback keeps a static vertex index, so a second parse in the same process overflows the vertex buffer on the valid triangle. The one-shot target preserves the pinned importer and supports file-based replay, Fandango, and AFL++. In-process libFuzzer campaigns are unsupported for this path.

## Run from the repository root

```sh
python3 parsarium.py build ascii_ply c brlcad
python3 parsarium.py run ascii_ply c brlcad controls/ascii_ply/triangle.ply
python3 parsarium.py replay ascii_ply c brlcad CORPUS_DIR runs/ascii_ply-brlcad-replay
python3 parsarium.py afl build ascii_ply c brlcad
python3 parsarium.py afl prepare ascii_ply c brlcad runs/ascii_ply-brlcad-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
