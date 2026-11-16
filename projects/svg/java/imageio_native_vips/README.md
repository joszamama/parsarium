# imageio-native-vips — SVG / Java

Pinned release: `2.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/java/imageio-native-vips/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg java imageio_native_vips
python3 parsarium.py run svg java imageio_native_vips controls/svg/red-green.svg
python3 parsarium.py replay svg java imageio_native_vips CORPUS_DIR runs/svg-imageio_native_vips-replay
python3 parsarium.py afl build svg java imageio_native_vips
python3 parsarium.py afl prepare svg java imageio_native_vips runs/svg-imageio_native_vips-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
