# ghostscript — PDF / C++

Pinned release: `10.08.0`. [Manifest](manifest.json)

[API, control result, and parser family](../../../../catalog/pdf/cpp/ghostscript/README.md)

The C++17 wrapper makes the same `gsapi_*` calls and runs the same PostScript program as [the catalog adapter](../../../../adapters/cpp/pdf/ghostscript.cpp): `.PDFInit`, `.PDFFile`, `.PDFInfo /NumPages`, `.PDFClose`. Ghostscript is built from the pinned GhostPDL source with LLVM coverage. The control check requires covered lines in the pdfi interpreter (`pdf/`) and in `pdf/pdf_xref.c`.

The wrapper accepts a page count only when the interpreter's whole output is that count followed by a newline. Like the adapter, it accepts zero.

The pinned one-page control covers 29,726 Ghostscript source lines, including 1,852 PDF interpreter lines and 128 lines in `pdf_xref.c`. The valid two-page control also passes the one-case runner. AFL++ reports 8,041 edges for one page and 8,046 for two pages; the latter adds five edge IDs.

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp ghostscript
python3 parsarium.py run pdf cpp ghostscript controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp ghostscript CORPUS_DIR runs/pdf-ghostscript-cpp-replay
python3 parsarium.py afl build pdf cpp ghostscript
python3 parsarium.py afl prepare pdf cpp ghostscript runs/pdf-ghostscript-cpp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
