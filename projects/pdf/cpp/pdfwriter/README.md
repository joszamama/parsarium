# pdfwriter — PDF / C++

Pinned release: `4.6.2`. [Manifest](manifest.json) · [source lock](source-lock.json)

[API, control result, and parser family](../../../../catalog/pdf/cpp/pdfwriter/README.md)

The harness writes the input bytes to a temporary file and calls the catalog API: `InputFile::OpenFile(path)`, `PDFParser::StartPDFParsing(file.GetInputStream())`, `PDFParser::GetPagesCount()`. A successful parse reports the page count; a zero-page document is accepted as `{"pages":0}`. Inputs over 1 MiB are rejected, matching the corpus bridge.

PDF-Writer is built from source twice as static libraries: once with LLVM source coverage for replay, once with ASan/UBSan for the libFuzzer entry. The build is in `build.sh`, so the AFL++ overlay instruments the parser library as well as the harness. DCT, TIFF, and PNG codecs are disabled, as in the catalog build.

The pinned one-page control covers 1,266 PDF-Writer source lines, including the PDF parser, tokenizer, object parser, and file input stream. The valid two-page control also passes the public one-case runner. AFL++ reports 1,292 edges for one page and 1,293 for two pages; the latter adds one edge ID.

## Run from the repository root

```sh
python3 parsarium.py build pdf cpp pdfwriter
python3 parsarium.py run pdf cpp pdfwriter controls/pdf/one-page.pdf
python3 parsarium.py replay pdf cpp pdfwriter CORPUS_DIR runs/pdf-pdfwriter-replay
python3 parsarium.py afl build pdf cpp pdfwriter
python3 parsarium.py afl prepare pdf cpp pdfwriter runs/pdf-pdfwriter-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
