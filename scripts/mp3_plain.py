"""Bounded structural checks for generated MPEG-1/2 Layer III streams, untagged or tagged."""

from __future__ import annotations


MAX_BYTES = 1 << 20
MPEG1_BITRATE_KBPS = (0, 32, 40, 48, 56, 64, 80, 96, 112, 128,
                      160, 192, 224, 256, 320)
MPEG2_BITRATE_KBPS = (0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96,
                      112, 128, 144, 160)
SAMPLE_RATES = {3: (44100, 48000, 32000), 2: (22050, 24000, 16000)}


def validate_frames(data: bytes) -> dict:
    """Require two or more contiguous, complete Layer III frames and no tags."""
    if not 8 <= len(data) <= MAX_BYTES:
        raise ValueError("plain MP3 output is outside the 8-byte to 1-MiB limit")
    if data.startswith(b"ID3") or (len(data) >= 128 and data[-128:-125] == b"TAG"):
        raise ValueError("plain MP3 output contains an ID3 tag")
    return layer_iii_frames(data, 0, len(data))


def validate_tagged(data: bytes) -> dict:
    """Require an ID3v2.3/2.4 tag, an ID3v1 trailer or both around contiguous Layer III frames."""
    if not 8 <= len(data) <= MAX_BYTES:
        raise ValueError("tagged MP3 output is outside the 8-byte to 1-MiB limit")
    start, end, version = 0, len(data), None
    if data.startswith(b"ID3"):
        if len(data) < 10 or data[3] not in (3, 4) or any(value & 0x80 for value in data[6:10]):
            raise ValueError("not an ID3v2.3 or ID3v2.4 header")
        start = 10 + ((data[6] << 21) | (data[7] << 14) | (data[8] << 7) | data[9])
        version = data[3]
    trailer = end - start >= 128 and data[end - 128:end - 125] == b"TAG"
    if trailer:
        end -= 128
    if version is None and not trailer:
        raise ValueError("tagged MP3 output has no ID3 tag")
    result = layer_iii_frames(data, start, end)
    result["kind"] = "id3_tagged_contiguous_layer_iii_headers"
    result["id3v2_version"] = f"2.{version}" if version else None
    result["id3v1"] = trailer
    return result


def layer_iii_frames(data: bytes, offset: int, end: int) -> dict:
    """Walk complete MPEG-1/2 Layer III frames from offset to end."""
    frames = 0
    stream = None
    while offset < end:
        if end - offset < 4:
            raise ValueError(f"incomplete MPEG frame header at byte {offset}")
        header = int.from_bytes(data[offset:offset + 4], "big")
        version = (header >> 19) & 0b11
        layer = (header >> 17) & 0b11
        bitrate_index = (header >> 12) & 0b1111
        sample_index = (header >> 10) & 0b11
        padding = (header >> 9) & 1
        if (header >> 21 != 0x7ff or version not in SAMPLE_RATES or layer != 1
                or bitrate_index in (0, 15) or sample_index == 3
                or header & 0b11 == 0b10):
            raise ValueError(f"not an MPEG-1/2 Layer III frame header at byte {offset}")
        sample_rate = SAMPLE_RATES[version][sample_index]
        if stream is None:
            stream = (version, sample_rate)
        elif stream != (version, sample_rate):
            raise ValueError(f"MPEG version or sample rate changes at byte {offset}")
        bitrates = MPEG1_BITRATE_KBPS if version == 3 else MPEG2_BITRATE_KBPS
        length = ((144000 if version == 3 else 72000) *
                  bitrates[bitrate_index]) // sample_rate + padding
        if offset + length > end:
            raise ValueError(f"incomplete MPEG frame at byte {offset}")
        offset += length
        frames += 1
    if frames < 2:
        raise ValueError("MP3 output has fewer than two complete frames")
    return {"kind": "contiguous_untagged_layer_iii_headers",
            "frames": frames, "mpeg_version": "1" if stream[0] == 3 else "2",
            "sample_rate": stream[1]}
