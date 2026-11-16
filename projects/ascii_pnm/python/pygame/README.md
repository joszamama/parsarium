# pygame — ASCII PNM / Python

Pinned release: `2.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/python/pygame/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm python pygame
python3 parsarium.py run ascii_pnm python pygame controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm python pygame CORPUS_DIR runs/ascii_pnm-pygame-replay
python3 parsarium.py afl build ascii_pnm python pygame
python3 parsarium.py afl prepare ascii_pnm python pygame runs/ascii_pnm-pygame-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Feedback scope:** AFL++ observes edges in the pinned `libSDL2_image-2-6bbdaa8d.0.so.0.2.3` shared library. This target does not claim source-line coverage. The verification receipt records the module hash and differential valid-control check.
