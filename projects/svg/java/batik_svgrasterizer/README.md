# batik-svgrasterizer — SVG / Java

Pinned release: `1.20`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/batik-svgrasterizer/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java batik_svgrasterizer
python3 parsarium.py run svg java batik_svgrasterizer controls/svg/red-green.svg
python3 parsarium.py replay svg java batik_svgrasterizer CORPUS_DIR runs/svg-batik_svgrasterizer-replay
python3 parsarium.py afl build svg java batik_svgrasterizer
python3 parsarium.py afl prepare svg java batik_svgrasterizer runs/svg-batik_svgrasterizer-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
