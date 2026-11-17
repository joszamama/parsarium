# codec-parser — MP3 / JavaScript

- **Pinned release:** `2.5.0`
- **License:** LGPL-3.0-or-later
- **Parsed scope:** Every MPEG Layer III frame of an untagged stream from a local Uint8Array, split by codec-parser's own frame-header parser: codec, layer, sample rate, channels, header-table bitrate, frame count, frame bytes, samples per frame, total samples, distinct header variants; no audio decode
- **Underlying family:** codec-parser JavaScript MPEG frame parser
- **Local input API:** `new CodecParser('audio/mpeg', { onCodecHeader }); parser.parseAll(Uint8Array) -> CodecFrame[] (header.sampleRate/channels/layer, samples, data, totalSamples)`
- **Documentation:** [API reference](<https://github.com/eshaz/codec-parser#readme>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3/parsers.json) · [control verification](../../../../data/javascript/mp3/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3/ranking.md)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)

## Observed control result

```json
{
  "codec": "mpeg",
  "layer": "Layer III",
  "sample_rate": 44100,
  "channels": 1,
  "bitrate": 64000,
  "frames": 11,
  "frame_bytes": 2298,
  "samples_per_frame": 1152,
  "total_samples": 12672,
  "header_variants": 1
}
```

Own frame-header parser (src/codecs/mpeg/MPEGHeader.js) and fixed-length frame sync that requires the next header at the computed frame length (src/codecs/Parser.js). The 2.5.0 tarball has no runtime dependencies and shares no code with mediabunny (separate author, repository and frame-sync design). Not one of the ten JavaScript paths selected in the former MP3-with-ID3v2 cell. Its ID3v2 probe skips tags without parsing them and is not exercised by the untagged controls. The same package also parses AAC, FLAC and Ogg; those parsers are not loaded for audio/mpeg frames beyond module import.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/javascript/codec_parser/README.md)

```sh
python3 parsarium.py build mp3 javascript codec_parser
python3 parsarium.py run mp3 javascript codec_parser controls/mp3/tone-44k-mono.mp3
```

**Coverage limit:** Untagged MPEG Layer III only; two valid CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, MPEG-2.5, ID3 or CRC-protected support. codec-parser splits frames and reads headers; it does not decode audio.
