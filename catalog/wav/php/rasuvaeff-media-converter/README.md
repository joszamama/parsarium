# rasuvaeff/media-converter — WAV / PHP

- **Pinned release:** `v1.2.0`
- **License:** BSD-3-Clause
- **Parsed scope:** PCM16 audio codec, 32 ms duration, container bit rate
- **Underlying family:** FFmpeg native RIFF/WAVE parser
- **Local input API:** `FfprobeMediaInfo::probe(local PCM WAV path); audio codec, duration, bit rate`
- **Documentation:** [API reference](<https://github.com/rasuvaeff/media-converter/blob/68ad862a4c6583ed5555a5815ee9bc0bd0568da4/src/FfprobeMediaInfo.php>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "audio_codec": "pcm_s16le",
  "duration_seconds": 0.032,
  "bit_rate": 139000
}
```

Typed wrapper invokes local FFprobe 9.0.2; distinct package path over shared FFmpeg family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
