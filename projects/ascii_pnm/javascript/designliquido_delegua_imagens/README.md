# @designliquido/delegua-imagens — ASCII PNM / JavaScript

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/ascii_pnm/javascript/designliquido-delegua-imagens/README.md)

## Run from the repository root

```sh
python3 parsarium.py build ascii_pnm javascript designliquido_delegua_imagens
python3 parsarium.py run ascii_pnm javascript designliquido_delegua_imagens controls/ascii_pnm/red-green.ppm
python3 parsarium.py replay ascii_pnm javascript designliquido_delegua_imagens CORPUS_DIR runs/ascii_pnm-designliquido_delegua_imagens-replay
python3 parsarium.py afl build ascii_pnm javascript designliquido_delegua_imagens
python3 parsarium.py afl prepare ascii_pnm javascript designliquido_delegua_imagens runs/ascii_pnm-designliquido_delegua_imagens-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
