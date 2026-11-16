# itext-kernel — PDF / Java

Pinned release: `9.8.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/java/itext-kernel/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf java itext_kernel
python3 parsarium.py run pdf java itext_kernel controls/pdf/one-page.pdf
python3 parsarium.py replay pdf java itext_kernel CORPUS_DIR runs/pdf-itext_kernel-replay
python3 parsarium.py afl build pdf java itext_kernel
python3 parsarium.py afl prepare pdf java itext_kernel runs/pdf-itext_kernel-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
