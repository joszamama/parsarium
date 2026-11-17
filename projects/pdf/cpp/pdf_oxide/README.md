# pdf_oxide — PDF / C++

Pinned release: `0.3.78`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/cpp/pdf-oxide/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp pdf_oxide
python3 parsarium.py run pdf cpp pdf_oxide controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp pdf_oxide CORPUS_DIR runs/pdf-pdf_oxide-replay
python3 parsarium.py afl build pdf cpp pdf_oxide
python3 parsarium.py afl prepare pdf cpp pdf_oxide runs/pdf-pdf_oxide-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** AFL++ pcguard guards cover the whole pdf_oxide crate, not only its syntax modules: stable rustc's sancov-module pass takes no source allowlist. Dependencies and the C++ harness are uninstrumented. The AFL++ target is one-shot /work/replay @@.
