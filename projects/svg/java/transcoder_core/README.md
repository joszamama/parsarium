# transcoder-core — SVG / Java

Pinned release: `0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/transcoder-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java transcoder_core
python3 parsarium.py run svg java transcoder_core controls/svg/red-green.svg
python3 parsarium.py replay svg java transcoder_core CORPUS_DIR runs/svg-transcoder_core-replay
python3 parsarium.py afl build svg java transcoder_core
python3 parsarium.py afl prepare svg java transcoder_core runs/svg-transcoder_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
