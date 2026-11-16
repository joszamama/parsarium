# github.com/aspose-pdf-foss/aspose-pdf-foss-for-go — PDF / Go

Pinned release: `v0.16.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/go/github-com-aspose-pdf-foss-aspose-pdf-foss-for-go/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf go github_com_aspose_pdf_foss_aspose_pdf_foss_for_go
python3 parsarium.py run pdf go github_com_aspose_pdf_foss_aspose_pdf_foss_for_go controls/pdf/one-page.pdf
python3 parsarium.py replay pdf go github_com_aspose_pdf_foss_aspose_pdf_foss_for_go CORPUS_DIR runs/pdf-github_com_aspose_pdf_foss_aspose_pdf_foss_for_go-replay
python3 parsarium.py afl build pdf go github_com_aspose_pdf_foss_aspose_pdf_foss_for_go
python3 parsarium.py afl prepare pdf go github_com_aspose_pdf_foss_aspose_pdf_foss_for_go runs/pdf-github_com_aspose_pdf_foss_aspose_pdf_foss_for_go-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
