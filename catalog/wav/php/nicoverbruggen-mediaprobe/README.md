# nicoverbruggen/mediaprobe — WAV / PHP

- **Pinned release:** `v1.1`
- **License:** MIT
- **Parsed scope:** WAV container name, 32 ms duration, 139 kb/s container bit rate
- **Underlying family:** FFmpeg native RIFF/WAVE parser
- **Local input API:** `MediaProbe(local PCM WAV path)::getMediaInfo(); format_name, parsed duration, bit rate`
- **Documentation:** [API reference](<https://github.com/nicoverbruggen/mediaprobe/blob/aa824d0691598dc9d66301f78da2687bc656884c/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "format": "wav",
  "duration_seconds": "0.032000",
  "bit_rate": "139000"
}
```

Composer wrapper delegates to local FFprobe 9.0.2; package path over the FFmpeg parser family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
