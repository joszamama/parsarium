# image/png.Decode(io.Reader) — PNG / Go

Pinned release: `1.27.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/go/png/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build png go stdlib_decode
python3 parsarium.py run png go stdlib_decode controls/png/red-green.png
python3 parsarium.py replay png go stdlib_decode CORPUS_DIR runs/png-stdlib_decode-replay
python3 parsarium.py afl build png go stdlib_decode
python3 parsarium.py afl prepare png go stdlib_decode runs/png-stdlib_decode-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
