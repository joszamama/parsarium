# resvg — SVG / C

Pinned release: `0.50.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/c/resvg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg c resvg
python3 parsarium.py run svg c resvg controls/svg/red-green.svg
python3 parsarium.py replay svg c resvg CORPUS_DIR runs/svg-resvg-replay
python3 parsarium.py afl build svg c resvg
python3 parsarium.py afl prepare svg c resvg runs/svg-resvg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** The AFL++ target uses one-shot /work/replay @@ because the selected C API parses a local file; parser-source feedback comes from usvg Rust code.
