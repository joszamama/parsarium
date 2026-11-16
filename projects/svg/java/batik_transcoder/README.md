# batik-transcoder — SVG / Java

Pinned release: `1.20`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/batik-transcoder/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java batik_transcoder
python3 parsarium.py run svg java batik_transcoder controls/svg/red-green.svg
python3 parsarium.py replay svg java batik_transcoder CORPUS_DIR runs/svg-batik_transcoder-replay
python3 parsarium.py afl build svg java batik_transcoder
python3 parsarium.py afl prepare svg java batik_transcoder runs/svg-batik_transcoder-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
