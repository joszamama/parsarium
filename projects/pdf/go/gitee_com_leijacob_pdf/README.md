# gitee.com/leijacob/pdf — PDF / Go

Pinned release: `v1.1.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/go/gitee-com-leijacob-pdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf go gitee_com_leijacob_pdf
python3 parsarium.py run pdf go gitee_com_leijacob_pdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf go gitee_com_leijacob_pdf CORPUS_DIR runs/pdf-gitee_com_leijacob_pdf-replay
python3 parsarium.py afl build pdf go gitee_com_leijacob_pdf
python3 parsarium.py afl prepare pdf go gitee_com_leijacob_pdf runs/pdf-gitee_com_leijacob_pdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
