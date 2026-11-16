# lodepng — PNG / C

Pinned release: `cci.20260102`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/c/lodepng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png c lodepng
python3 parsarium.py run png c lodepng controls/png/red-green.png
python3 parsarium.py replay png c lodepng CORPUS_DIR runs/png-lodepng-replay
python3 parsarium.py afl build png c lodepng
python3 parsarium.py afl prepare png c lodepng runs/png-lodepng-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
