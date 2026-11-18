# PYTHON × PDF: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

PyPI Stats last_month downloads excluding known mirrors.

| Rank | Package | Release | PyPI downloads (last month) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [pypdf](https://pypdf.readthedocs.io/en/latest/modules/PdfReader.html) | 7.0.1 | 125,991,621 | page text | pypdf pure Python |
| 2 | [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/how-to-open-a-file.html) | 2.1 | 83,199,606 | page text | MuPDF |
| 3 | [pypdfium2](https://pypdfium2.readthedocs.io/en/stable/python_api.html) | 5.10.1 | 61,857,655 | page text | PDFium |
| 4 | [pdfminer.six](https://pdfminersix.readthedocs.io/en/latest/tutorial/highlevel.html) | 20260107 | 53,178,551 | page text | pdfminer.six |
| 5 | [pdfplumber](https://github.com/jsvine/pdfplumber) | 0.11.10 | 40,689,748 | page text | pdfplumber via pdfminer.six |
| 6 | [pdf2image](https://github.com/Belval/pdf2image) | 1.17.0 | 16,169,954 | rendered page dimensions | Poppler pdftoppm subprocess |
| 7 | [markitdown](https://pypi.org/project/markitdown/0.1.9/) | 0.1.9 | 14,569,559 | page text as Markdown | MarkItDown via pdfplumber/pdfminer.six |
| 8 | [pikepdf](https://pikepdf.readthedocs.io/en/latest/tutorial.html) | 10.18.0 | 9,480,221 | page count and document title | QPDF |
| 9 | [pdfrw](https://github.com/pmaupin/pdfrw) | 0.4 | 3,195,794 | page count and document title | pdfrw parser |
| 10 | [pdf2docx](https://github.com/ArtifexSoftware/pdf2docx/blob/master/pdf2docx/converter.py) | 0.5.13 | 1,208,898 | parsed page sections | pdf2docx layout over MuPDF |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
