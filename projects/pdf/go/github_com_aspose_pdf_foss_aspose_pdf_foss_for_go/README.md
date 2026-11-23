# github.com/aspose-pdf-foss/aspose-pdf-foss-for-go — PDF / Go

Pinned release: `v0.16.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/go/github-com-aspose-pdf-foss-aspose-pdf-foss-for-go/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf go github_com_aspose_pdf_foss_aspose_pdf_foss_for_go
python3 parsarium.py run pdf go github_com_aspose_pdf_foss_aspose_pdf_foss_for_go controls/pdf/one-page.pdf
python3 parsarium.py replay pdf go github_com_aspose_pdf_foss_aspose_pdf_foss_for_go CORPUS_DIR runs/pdf-github_com_aspose_pdf_foss_aspose_pdf_foss_for_go-replay
python3 parsarium.py fandango setup
python3 parsarium.py afl build pdf go github_com_aspose_pdf_foss_aspose_pdf_foss_for_go
python3 parsarium.py afl prepare pdf go github_com_aspose_pdf_foss_aspose_pdf_foss_for_go runs/pdf-github_com_aspose_pdf_foss_aspose_pdf_foss_for_go-afl --fandango 100
python3 parsarium.py afl run runs/pdf-github_com_aspose_pdf_foss_aspose_pdf_foss_for_go-afl --seconds 600
```

Replace `CORPUS_DIR` with a directory of matching files. `afl prepare --fandango 100` seeds the run with the control and 100 valid inputs generated from the format's default Fandango spec, and `plan.json` records the spec, its SHA-256, the random seed and the Fandango version. Without `--fandango`, the control is the only seed. `afl run` starts a bounded campaign; add `--check` to verify the plan without starting it.
