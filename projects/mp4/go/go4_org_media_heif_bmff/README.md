# go4.org/media/heif/bmff — MP4 / Go

Pinned release: `v0.0.0-20261028031214-ed6929a230fe`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/go/go4-org-media-heif-bmff/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 go go4_org_media_heif_bmff
python3 parsarium.py run mp4 go go4_org_media_heif_bmff controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 go go4_org_media_heif_bmff CORPUS_DIR runs/mp4-go4_org_media_heif_bmff-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build mp4 go go4_org_media_heif_bmff
python3 parsarium.py afl prepare mp4 go go4_org_media_heif_bmff runs/mp4-go4_org_media_heif_bmff-afl --fandango 100
python3 parsarium.py afl run runs/mp4-go4_org_media_heif_bmff-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
