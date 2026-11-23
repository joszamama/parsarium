"""Read PDF bytes through pdfrw and consume page count and title."""

from pdfrw import PdfReader
from pdfrw.errors import PdfParseError


def parse_pdf(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    reader = PdfReader(fdata=data)
    pages = len(reader.pages)
    # A file without /Info or without /Info /Title has no title: report null, not str(None).
    title = reader.Info.Title if reader.Info else None
    return {"pages": pages, "title": None if title is None else str(title).strip("()")}


def fuzz_one_input(data: bytes):
    try:
        parse_pdf(data)
    except PdfParseError:
        pass
