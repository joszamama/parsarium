# batik-codec — PNG / Java

Pinned release: `1.20`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/java/batik-codec/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png java batik_codec
python3 parsarium.py run png java batik_codec controls/png/red-green.png
python3 parsarium.py replay png java batik_codec CORPUS_DIR runs/png-batik_codec-replay
python3 parsarium.py afl build png java batik_codec
python3 parsarium.py afl prepare png java batik_codec runs/png-batik_codec-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
