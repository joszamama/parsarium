# github.com/JoshVarga/svgparser — SVG / Go

Pinned release: `v0.0.0-20200804023048-5eaba627a7d1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/svg/go/github-com-joshvarga-svgparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build svg go github_com_joshvarga_svgparser
python3 parsarium.py run svg go github_com_joshvarga_svgparser controls/svg/red-green.svg
python3 parsarium.py replay svg go github_com_joshvarga_svgparser CORPUS_DIR runs/svg-github_com_joshvarga_svgparser-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build svg go github_com_joshvarga_svgparser
python3 parsarium.py afl prepare svg go github_com_joshvarga_svgparser runs/svg-github_com_joshvarga_svgparser-afl --fandango 100
python3 parsarium.py afl run runs/svg-github_com_joshvarga_svgparser-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
