# kiwilan/php-audio — WAV / PHP

- **Pinned release:** `4.0.02`
- **License:** MIT
- **Parsed scope:** RIFF/WAVE PCM16 format, 8 kHz sample rate, mono channel count and PCM codec
- **Underlying family:** getID3 native RIFF/WAVE parser
- **Local input API:** `Audio::read(local PCM WAV path)->getMetadata(); data format, sample rate, channels, codec`
- **Documentation:** [API reference](<https://github.com/kiwilan/php-audio/blob/684002b34e5db3fa2935d6b9ba8cba0ebd81b1a7/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "format": "wav",
  "sample_rate": 8000,
  "channels": 1,
  "codec": "Pulse Code Modulation (PCM)"
}
```

Metadata comes from pinned getID3. Audio::isValid() is false because the control has no selected tags; header metadata still parses.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
