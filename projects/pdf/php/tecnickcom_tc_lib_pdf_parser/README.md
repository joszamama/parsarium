# tecnickcom/tc-lib-pdf-parser — PDF / PHP

Pinned release: `3.16.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/tecnickcom-tc-lib-pdf-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php tecnickcom_tc_lib_pdf_parser
python3 parsarium.py run pdf php tecnickcom_tc_lib_pdf_parser controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php tecnickcom_tc_lib_pdf_parser CORPUS_DIR runs/pdf-tecnickcom_tc_lib_pdf_parser-replay
python3 parsarium.py afl build pdf php tecnickcom_tc_lib_pdf_parser
python3 parsarium.py afl prepare pdf php tecnickcom_tc_lib_pdf_parser runs/pdf-tecnickcom_tc_lib_pdf_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
