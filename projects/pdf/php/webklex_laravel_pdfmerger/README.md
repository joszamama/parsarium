# webklex/laravel-pdfmerger — PDF / PHP

Pinned release: `1.3.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/webklex-laravel-pdfmerger/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php webklex_laravel_pdfmerger
python3 parsarium.py run pdf php webklex_laravel_pdfmerger controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php webklex_laravel_pdfmerger CORPUS_DIR runs/pdf-webklex_laravel_pdfmerger-replay
python3 parsarium.py afl build pdf php webklex_laravel_pdfmerger
python3 parsarium.py afl prepare pdf php webklex_laravel_pdfmerger runs/pdf-webklex_laravel_pdfmerger-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
