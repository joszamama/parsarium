# imageio-pnm — ASCII PNM / Java

Pinned release: `3.15.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/java/imageio-pnm/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm java imageio_pnm
python3 parsarium.py run ascii_pnm java imageio_pnm controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm java imageio_pnm CORPUS_DIR runs/ascii_pnm-imageio_pnm-replay
python3 parsarium.py afl build ascii_pnm java imageio_pnm
python3 parsarium.py afl prepare ascii_pnm java imageio_pnm runs/ascii_pnm-imageio_pnm-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
