# github.com/lafriks/go-svg — SVG / Go

Pinned release: `v0.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-lafriks-go-svg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go github_com_lafriks_go_svg
python3 parsarium.py run svg go github_com_lafriks_go_svg controls/svg/red-green.svg
python3 parsarium.py replay svg go github_com_lafriks_go_svg CORPUS_DIR runs/svg-github_com_lafriks_go_svg-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg go github_com_lafriks_go_svg
python3 parsarium.py afl prepare svg go github_com_lafriks_go_svg runs/svg-github_com_lafriks_go_svg-afl --fandango 100
python3 parsarium.py afl run runs/svg-github_com_lafriks_go_svg-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
