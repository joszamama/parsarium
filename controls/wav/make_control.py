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
