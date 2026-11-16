# magento/zend-pdf — PDF / PHP

Pinned release: `1.16.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/magento-zend-pdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php magento_zend_pdf
python3 parsarium.py run pdf php magento_zend_pdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php magento_zend_pdf CORPUS_DIR runs/pdf-magento_zend_pdf-replay
python3 parsarium.py afl build pdf php magento_zend_pdf
python3 parsarium.py afl prepare pdf php magento_zend_pdf runs/pdf-magento_zend_pdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
