# github.com/andrianbdn/iospng — PNG / Go

Pinned release: `v0.0.0-20180730113000-dccef1992541`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/go/github-com-andrianbdn-iospng/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png go github_com_andrianbdn_iospng
python3 parsarium.py run png go github_com_andrianbdn_iospng controls/png/red-green.png
python3 parsarium.py replay png go github_com_andrianbdn_iospng CORPUS_DIR runs/png-github_com_andrianbdn_iospng-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build png go github_com_andrianbdn_iospng
python3 parsarium.py afl prepare png go github_com_andrianbdn_iospng runs/png-github_com_andrianbdn_iospng-afl --fandango 100
python3 parsarium.py afl run runs/png-github_com_andrianbdn_iospng-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
