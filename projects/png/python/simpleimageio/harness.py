"""One input invokes the pinned SimpleImageIO PNG reader."""

from adapter import parse_data


def fuzz_one_input(data: bytes) -> None:
    try:
        parse_data(data)
    except (OSError, ValueError, IndexError):
        return
