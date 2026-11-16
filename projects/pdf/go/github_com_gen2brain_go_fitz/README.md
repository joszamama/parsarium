# github.com/gen2brain/go-fitz — PDF / Go

Pinned release: `v1.28.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/go/github-com-gen2brain-go-fitz/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf go github_com_gen2brain_go_fitz
python3 parsarium.py run pdf go github_com_gen2brain_go_fitz controls/pdf/one-page.pdf
python3 parsarium.py replay pdf go github_com_gen2brain_go_fitz CORPUS_DIR runs/pdf-github_com_gen2brain_go_fitz-replay
python3 parsarium.py afl build pdf go github_com_gen2brain_go_fitz
python3 parsarium.py afl prepare pdf go github_com_gen2brain_go_fitz runs/pdf-github_com_gen2brain_go_fitz-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
