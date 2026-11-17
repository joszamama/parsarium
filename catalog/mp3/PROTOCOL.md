# MP3 cell protocol

This cell applies the [general protocol](../../PROTOCOL.md) to MP3 files, with or without an ID3v2 tag. It replaces the former "MP3 with ID3v2" format and the plain-MP3 pilot. Each ecosystem keeps at most ten paths, chosen from the paths selected in either former cell; the [merge record](../../data/curation/mp3-merge.json) lists every kept, removed and duplicate path.

## Eligibility

A path qualifies on one of two controls, and its parser record names which (`control_kind`):

- **ID3v2-tagged control** (`id3v2_tagged`): the path reads `controls/mp3_id3v2/tone-tags.mp3` from local bytes, a local file or a stream and reports ID3v2 fields (for example title and artist) or audio-stream properties parsed from the file.
- **Untagged frame controls** (`untagged_frames`): the path reads MPEG audio frames and reports a frame-derived result such as frame count, frame bytes, sample rate, channels, decoded samples or a frame-derived duration. A result that could come from a tag or the file size alone does not count.

Encoders, signature detectors and codec-string parsers are excluded. Tag readers and frame decoders share one ranking; the cell does not claim that each path parses both the tag and the audio frames.

## Controls

- `controls/mp3_id3v2/tone-tags.mp3`: valid MP3 with an ID3v2.3 tag.
- `controls/mp3/tone-44k-mono.mp3`: 0.25 s of 440 Hz, MPEG-1 Layer III, 44.1 kHz mono at 64 kbit/s CBR, 11 frames in 2,298 bytes.
- `controls/mp3/tone-22k-stereo.mp3`: the second untagged control for AFL++ feedback. 0.25 s of 660 Hz, MPEG-2 Layer III, 22.05 kHz stereo at 32 kbit/s CBR, 12 frames in 1,254 bytes.

The untagged files begin with a frame sync. `controls/mp3/check_controls.py` walks the four-byte headers to EOF and serves as an independent oracle for the frame counts. ffprobe 9.0.2 `-count_frames` gives the same counts.

## Adoption

Paths are ranked within one ecosystem by its registry metric, under the [ten-path selection plan](../../data/curation/plan.json). Where the two former cells together held more than ten paths (C, Go, JavaScript, Python), all of their paths were re-ranked from one fresh capture recorded as `merged_mp3_ranking_2026_11_17` in `data/<ecosystem>/mp3/registry-snapshot.json`. The same package selected in both former cells counts once. Facade crates and wrappers keep their shared parser family in the record. The cell is not padded.

## Target names

Targets verified on the tagged control keep the project directory `projects/mp3_id3v2/` and the command-line format `mp3_id3v2`, because their pinned manifests and receipts record those paths. `data/<ecosystem>/mp3_id3v2/` holds links into this cell for those manifests; it is not a catalog cell. The evidence of the former plain-MP3 pilot is kept in `data/<ecosystem>/mp3/plain-mp3-pilot/`.

## AFL++

The overlay must show parser-derived feedback. Untagged-frame paths run each of the two controls three times under `afl-showmap`, and the receipt records the edge counts, stable edges, and edges unique to each control. The overlay checks only launchers and feedback. It runs no campaign and tests no malformed inputs.
