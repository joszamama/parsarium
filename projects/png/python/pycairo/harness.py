"""One input invokes the pinned Pycairo PNG loader."""

from adapter import parse_data
import cairo


def fuzz_one_input(data: bytes) -> None:
    try:
        parse_data(data)
    except (cairo.Error, OSError, ValueError, IndexError):
        return
