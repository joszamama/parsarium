# gnome-papers — PDF / C

Pinned release: `51.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/c/gnome-papers/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf c gnome-papers
python3 parsarium.py run pdf c gnome-papers controls/pdf/two-page.pdf
python3 parsarium.py replay pdf c gnome-papers CORPUS_DIR runs/pdf-gnome-papers-replay
python3 parsarium.py afl build pdf c gnome-papers
python3 parsarium.py afl prepare pdf c gnome-papers runs/pdf-gnome-papers-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** The byte-input fuzz bridge accepts at most 1 MiB per case before writing a temporary PDF. The documented local-file API is not subject to this bridge limit. AFL uses one-shot replay because Papers has process-global backend state.

**Native engine limit:** This target starts a fresh process for each input. In-process native fuzzing is unsupported; use one-input replay or the prepared AFL++ run.
