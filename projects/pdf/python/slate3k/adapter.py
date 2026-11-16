"""Parse the pinned PDF control with Slate3k."""
import slate3k


def parse(name, path):
    with open(path, "rb") as stream:
        pages = slate3k.PDF(stream)
    return {"pages": len(pages), "text": " ".join(pages[0].split())}
