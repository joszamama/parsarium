# pygame — PNG / Python

Pinned release: `2.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/python/pygame/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png python pygame
python3 parsarium.py run png python pygame controls/png/red-green.png
python3 parsarium.py replay png python pygame CORPUS_DIR runs/png-pygame-replay
python3 parsarium.py afl build png python pygame
python3 parsarium.py afl prepare png python pygame runs/png-pygame-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Feedback scope:** AFL++ observes edges in the pinned `libpng16-bb793e21.so.16.37.0` shared library. This target does not claim source-line coverage. The verification receipt records the module hash and differential valid-control check.
