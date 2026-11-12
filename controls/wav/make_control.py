"""Generate a deterministic valid mono PCM RIFF/WAVE control."""

from pathlib import Path
import struct


ROOT = Path(__file__).resolve().parent
samples = (0, 1000, -1000, 0)
payload = struct.pack("<4h", *samples)
format_chunk = struct.pack("<HHIIHH", 1, 1, 8000, 16000, 2, 16)
chunks = b"fmt " + struct.pack("<I", len(format_chunk)) + format_chunk
chunks += b"data" + struct.pack("<I", len(payload)) + payload
output = b"RIFF" + struct.pack("<I", len(chunks) + 4) + b"WAVE" + chunks
(ROOT / "four-samples.wav").write_bytes(output)
print(f"Wrote {len(output)} bytes")

# Some readers require enough bytes to fill a fixed header buffer or reject
# extremely short recordings. This remains a small, valid PCM/WAVE control.
extended_samples = samples + (0,) * 252
extended_payload = struct.pack("<256h", *extended_samples)
extended_chunks = b"fmt " + struct.pack("<I", len(format_chunk)) + format_chunk
extended_chunks += b"data" + struct.pack("<I", len(extended_payload)) + extended_payload
extended = b"RIFF" + struct.pack("<I", len(extended_chunks) + 4) + b"WAVE" + extended_chunks
(ROOT / "256-samples.wav").write_bytes(extended)
print(f"Wrote {len(extended)} bytes")

# MediaInfo JNA's file API requires at least 65,536 bytes. This valid PCM/WAVE
# control has the same first samples and format with silence for the remainder.
media_info_samples = samples + (0,) * (32768 - len(samples))
media_info_payload = struct.pack("<32768h", *media_info_samples)
media_info_chunks = b"fmt " + struct.pack("<I", len(format_chunk)) + format_chunk
media_info_chunks += b"data" + struct.pack("<I", len(media_info_payload)) + media_info_payload
media_info_control = b"RIFF" + struct.pack("<I", len(media_info_chunks) + 4) + b"WAVE" + media_info_chunks
(ROOT / "32768-samples.wav").write_bytes(media_info_control)
print(f"Wrote {len(media_info_control)} bytes")
