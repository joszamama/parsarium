# github.com/gen2brain/go-fitz — PDF / Go

Pinned release: `v1.28.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/go/github-com-gen2brain-go-fitz/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf go github_com_gen2brain_go_fitz
python3 parsarium.py run pdf go github_com_gen2brain_go_fitz controls/pdf/one-page.pdf
python3 parsarium.py replay pdf go github_com_gen2brain_go_fitz CORPUS_DIR runs/pdf-github_com_gen2brain_go_fitz-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build pdf go github_com_gen2brain_go_fitz
python3 parsarium.py afl prepare pdf go github_com_gen2brain_go_fitz runs/pdf-github_com_gen2brain_go_fitz-afl --fandango 100
python3 parsarium.py afl run runs/pdf-github_com_gen2brain_go_fitz-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
