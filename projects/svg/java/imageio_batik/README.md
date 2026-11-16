# imageio-batik — SVG / Java

Pinned release: `3.15.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/imageio-batik/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java imageio_batik
python3 parsarium.py run svg java imageio_batik controls/svg/red-green.svg
python3 parsarium.py replay svg java imageio_batik CORPUS_DIR runs/svg-imageio_batik-replay
python3 parsarium.py afl build svg java imageio_batik
python3 parsarium.py afl prepare svg java imageio_batik runs/svg-imageio_batik-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
