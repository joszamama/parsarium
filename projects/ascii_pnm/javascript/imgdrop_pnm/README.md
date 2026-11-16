# @imgdrop/pnm — ASCII PNM / JavaScript

Pinned release: `1.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/javascript/imgdrop-pnm/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm javascript imgdrop_pnm
python3 parsarium.py run ascii_pnm javascript imgdrop_pnm controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm javascript imgdrop_pnm CORPUS_DIR runs/ascii_pnm-imgdrop_pnm-replay
python3 parsarium.py afl build ascii_pnm javascript imgdrop_pnm
python3 parsarium.py afl prepare ascii_pnm javascript imgdrop_pnm runs/ascii_pnm-imgdrop_pnm-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
