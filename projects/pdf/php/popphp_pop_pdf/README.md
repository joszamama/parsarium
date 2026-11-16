# popphp/pop-pdf — PDF / PHP

Pinned release: `6.2.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/popphp-pop-pdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php popphp_pop_pdf
python3 parsarium.py run pdf php popphp_pop_pdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php popphp_pop_pdf CORPUS_DIR runs/pdf-popphp_pop_pdf-replay
python3 parsarium.py afl build pdf php popphp_pop_pdf
python3 parsarium.py afl prepare pdf php popphp_pop_pdf runs/pdf-popphp_pop_pdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
