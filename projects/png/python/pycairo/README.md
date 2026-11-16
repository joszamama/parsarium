# pycairo — PNG / Python

Pinned release: `1.29.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/pycairo/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python pycairo
python3 parsarium.py run png python pycairo controls/png/red-green.png
python3 parsarium.py replay png python pycairo CORPUS_DIR runs/png-pycairo-replay
python3 parsarium.py afl build png python pycairo
python3 parsarium.py afl prepare png python pycairo runs/png-pycairo-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Feedback scope:** AFL++ observes edges in the pinned `libpng16.so.16` shared library. This target does not claim source-line coverage. The verification receipt records the module hash and differential valid-control check.
