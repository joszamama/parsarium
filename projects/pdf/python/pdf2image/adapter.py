"""Run one documented local PDF input path and print its parsed control fields."""

import json
import sys


def text(value):
    return " ".join(str(value).split())


def parse(name, path):
    if name == "pypdf":
        from pypdf import PdfReader
        doc = PdfReader(path)
        return {"pages": len(doc.pages), "text": text(doc.pages[0].extract_text())}
    if name == "pdfrw":
        from pdfrw import PdfReader
        doc = PdfReader(path)
        return {"pages": len(doc.pages), "title": str(doc.Info.Title).strip("()")}
    if name == "pdfminer.six":
        from pdfminer.high_level import extract_text
        return {"text": text(extract_text(path))}
    if name == "pdfplumber":
        import pdfplumber
        with pdfplumber.open(path) as doc:
            return {"pages": len(doc.pages), "text": text(doc.pages[0].extract_text())}
    if name == "PyMuPDF":
        import pymupdf
        with pymupdf.open(path) as doc:
            return {"pages": len(doc), "text": text(doc[0].get_text())}
    if name == "pypdfium2":
        import pypdfium2
        doc = pypdfium2.PdfDocument(path)
        try:
            return {"pages": len(doc), "text": text(doc[0].get_textpage().get_text_range())}
        finally:
            doc.close()
    if name == "pikepdf":
        import pikepdf
        with pikepdf.open(path) as doc:
            return {"pages": len(doc.pages), "title": str(doc.docinfo["/Title"])}
    if name == "pdfquery":
        import pdfquery
        doc = pdfquery.PDFQuery(path)
        doc.load()
        return {"pages": len(doc.tree.findall(".//LTPage")),
                "text": text(doc.tree.xpath("string(.//LTTextLineHorizontal)"))}
    if name == "pdf2image":
        from pdf2image import convert_from_path, pdfinfo_from_path
        # Render page 1 for its size; the page count comes from pdf2image's
        # pdfinfo_from_path, not from the one page rendered.
        pages = convert_from_path(path, first_page=1, last_page=1)
        info = pdfinfo_from_path(path)
        return {"pages": info["Pages"], "width": pages[0].width, "height": pages[0].height}
    if name == "PyPDF4":
        from PyPDF4 import PdfFileReader
        with open(path, "rb") as stream:
            doc = PdfFileReader(stream)
            return {"pages": doc.getNumPages(), "title": str(doc.getDocumentInfo().title)}
    if name == "pdf_oxide":
        from pdf_oxide import PdfDocument
        with PdfDocument(path) as doc:
            return {"pages": len(doc), "text": text(doc[0].text)}
    if name == "pymupdf4llm":
        import pymupdf4llm
        return {"text": text(pymupdf4llm.to_markdown(path))}
    if name == "pdf2docx":
        from pdf2docx import Converter
        doc = Converter(path)
        try:
            doc.parse(**doc.default_settings)
            return {"pages": len(doc.pages), "parsed_sections": len(doc.pages[0].sections)}
        finally:
            doc.close()
    if name == "pdftext":
        from pdftext.extraction import plain_text_output
        return {"text": text(plain_text_output(path))}
    if name == "markitdown":
        from markitdown import MarkItDown
        return {"text": text(MarkItDown().convert(path).markdown)}
    if name == "paper2md":
        from paper2md import convert
        return {"text": text(convert(path).markdown)}
    if name == "pdfnaut":
        from pdfnaut import PdfDocument
        doc = PdfDocument.from_filename(path)
        return {"pages": len(doc.pages), "title": str(doc.doc_info.title)}
    if name == "pdftotext":
        import pdftotext
        with open(path, "rb") as stream:
            doc = pdftotext.PDF(stream)
            return {"pages": len(doc), "text": text(doc[0])}
    raise ValueError(f"unknown PDF adapter: {name}")


if __name__ == "__main__":
    print(json.dumps(parse(sys.argv[1], sys.argv[2]), sort_keys=True))
