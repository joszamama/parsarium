# MP3 cell protocol

This cell applies the [general protocol](../../PROTOCOL.md) to plain MP3: a stream of MPEG audio frames with no ID3v2 prefix, ID3v1 trailer, or Xing/Info frame. It is separate from [MP3 with ID3v2](../mp3_id3v2/README.md), where a tag reader can pass without touching audio frames.

## Eligibility

A path qualifies only if it reads MPEG audio frames from local bytes, a local file, or a stream. Tag-only readers, encoders, signature detectors, and codec-string parsers are excluded and listed as such in `data/<ecosystem>/mp3/leads.json`.

The observed result must come from the frames. Valid results are frame count, frame bytes, sample rate, channels, decoded samples, or a frame-derived duration. A result that could be produced from a tag or a file size alone is not accepted.

## Controls

- `controls/mp3/tone-44k-mono.mp3`: the primary control. It is 0.25 s of 440 Hz, MPEG-1 Layer III, 44.1 kHz mono at 64 kbit/s CBR, with 11 frames in 2,298 bytes.
- `controls/mp3/tone-22k-stereo.mp3`: the fixed second control for AFL++ feedback. It is 0.25 s of 660 Hz, MPEG-2 Layer III, 22.05 kHz stereo at 32 kbit/s CBR, with 12 frames in 1,254 bytes.

Both files are untagged and begin with a frame sync. `controls/mp3/check_controls.py` walks the four-byte headers to EOF and serves as an independent oracle for the frame counts. ffprobe 9.0.2 `-count_frames` gives the same counts.

## Adoption

Paths are ranked within one ecosystem by its registry metric. For Rust, this is the crates.io 90-day recent downloads returned by the recorded search snapshot. Facade crates that re-export a selected parser are recorded as shared-family leads. The ceiling is ten paths, and the cell is not padded.

## AFL++

The overlay must show parser-derived feedback on both controls. Each control runs three times under `afl-showmap`, and the receipt records the edge counts, stable edges, and edges unique to each control. The overlay checks only launchers and feedback. It runs no campaign and tests no malformed inputs.
