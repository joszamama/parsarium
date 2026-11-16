"""Decode PNG bytes with the pinned SimpleImageIO native reader."""

from pathlib import Path
import tempfile


def parse_data(data: bytes) -> dict:
    import simpleimageio

    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "input.png"
        source.write_bytes(data)
        image = simpleimageio.read(str(source))
    if len(image.shape) != 3 or image.shape[2] != 4:
        raise ValueError(f"expected an RGBA PNG, got shape {image.shape}")

    def rgba(row):
        return [round(float(channel) * 255) for channel in row]

    return {
        "width": int(image.shape[1]),
        "height": int(image.shape[0]),
        "rgba0": rgba(image[0, 0]),
        "rgba1": rgba(image[0, 1]),
    }
