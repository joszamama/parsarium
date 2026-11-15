"""Read PDF bytes through pdfrw and consume page count and title."""

from pdfrw import PdfReader
from pdfrw.errors import PdfParseError


def parse_pdf(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    reader = PdfReader(fdata=data)
    pages = len(reader.pages)
    title = str(reader.Info.Title).strip("()") if reader.Info else ""
    return {"pages": pages, "title": title}


def fuzz_one_input(data: bytes):
    try:
        parse_pdf(data)
    except PdfParseError:
        pass
