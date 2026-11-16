"""Parse the pinned PDF control with PDFx."""
import pdfx


def parse(name, path):
    metadata = pdfx.PDFx(str(path)).get_metadata()
    return {"pages": metadata["Pages"], "title": metadata["Title"]}
