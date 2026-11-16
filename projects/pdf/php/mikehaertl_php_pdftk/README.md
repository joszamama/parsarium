# mikehaertl/php-pdftk — PDF / PHP

Pinned release: `0.14.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/mikehaertl-php-pdftk/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php mikehaertl_php_pdftk
python3 parsarium.py run pdf php mikehaertl_php_pdftk controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php mikehaertl_php_pdftk CORPUS_DIR runs/pdf-mikehaertl_php_pdftk-replay
python3 parsarium.py afl build pdf php mikehaertl_php_pdftk
python3 parsarium.py afl prepare pdf php mikehaertl_php_pdftk runs/pdf-mikehaertl_php_pdftk-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
