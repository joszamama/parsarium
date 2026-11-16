# office-text-extractor — PDF / JavaScript

Pinned release: `4.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/javascript/office-text-extractor/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf javascript office_text_extractor
python3 parsarium.py run pdf javascript office_text_extractor controls/pdf/one-page.pdf
python3 parsarium.py replay pdf javascript office_text_extractor CORPUS_DIR runs/pdf-office_text_extractor-replay
python3 parsarium.py afl build pdf javascript office_text_extractor
python3 parsarium.py afl prepare pdf javascript office_text_extractor runs/pdf-office_text_extractor-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
