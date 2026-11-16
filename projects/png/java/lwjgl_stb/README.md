# lwjgl-stb — PNG / Java

Pinned release: `3.4.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/lwjgl-stb/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java lwjgl_stb
python3 parsarium.py run png java lwjgl_stb controls/png/red-green.png
python3 parsarium.py replay png java lwjgl_stb CORPUS_DIR runs/png-lwjgl_stb-replay
python3 parsarium.py afl build png java lwjgl_stb
python3 parsarium.py afl prepare png java lwjgl_stb runs/png-lwjgl_stb-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
