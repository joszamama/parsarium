# ghostscript — PDF / C

Pinned release: `10.08.0`. [Manifest](manifest.json) · [Docker receipt](verification.json) · [AFL++ receipt](../../../../fuzzing/afl-native/pdf/c/ghostscript/verification.json)

[API, control result, and parser family](../../../../catalog/pdf/c/ghostscript/README.md)

The one-page PDF control passed Docker replay and one-case fuzzer smoke; a separate valid zero-page PDF reports zero pages. LLVM coverage reached 29,797 lines in pinned Ghostscript source, including 1,852 lines in its PDF interpreter. The source-built AFL++ overlay reported 8,020 feedback edges on the control. Repeat maps matched; a valid two-page PDF changed five edge IDs. Ghostscript's public C API loads a local file through its PDF interpreter and reports the parsed `/NumPages` value. The base libFuzzer binary has harness feedback only; use the AFL++ overlay for parser steering.

## Run from the repository root

```sh
python3 parsarium.py build pdf c ghostscript
python3 parsarium.py run pdf c ghostscript controls/pdf/one-page.pdf
python3 parsarium.py replay pdf c ghostscript CORPUS_DIR runs/pdf-ghostscript-replay
python3 parsarium.py afl build pdf c ghostscript
python3 parsarium.py afl prepare pdf c ghostscript runs/pdf-ghostscript-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
