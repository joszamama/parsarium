"""Read PDF bytes through pypdf and consume the first page's text."""

from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError


def parse_pdf(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    reader = PdfReader(BytesIO(data))
    pages = len(reader.pages)
    text = (reader.pages[0].extract_text() or "").strip() if pages else ""
    return {"pages": pages, "text": text}


def fuzz_one_input(data: bytes):
    try:
        parse_pdf(data)
    except PdfReadError:
        pass
