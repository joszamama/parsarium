# ijp-imageio — ASCII PNM / Java

Pinned release: `2.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/java/ijp-imageio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm java ijp_imageio
python3 parsarium.py run ascii_pnm java ijp_imageio controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm java ijp_imageio CORPUS_DIR runs/ascii_pnm-ijp_imageio-replay
python3 parsarium.py afl build ascii_pnm java ijp_imageio
python3 parsarium.py afl prepare ascii_pnm java ijp_imageio runs/ascii_pnm-ijp_imageio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
