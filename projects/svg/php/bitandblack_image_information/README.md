# bitandblack/image-information — SVG / PHP

Pinned release: `3.3.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/php/bitandblack-image-information/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg php bitandblack_image_information
python3 parsarium.py run svg php bitandblack_image_information controls/svg/red-green.svg
python3 parsarium.py replay svg php bitandblack_image_information CORPUS_DIR runs/svg-bitandblack_image_information-replay
python3 parsarium.py afl build svg php bitandblack_image_information
python3 parsarium.py afl prepare svg php bitandblack_image_information runs/svg-bitandblack_image_information-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
