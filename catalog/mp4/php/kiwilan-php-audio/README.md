# kiwilan/php-audio — MP4 / PHP

- **Pinned release:** `4.0.02`
- **License:** MIT
- **Parsed scope:** MP4 container and 8 kHz mono AAC audio track
- **Underlying family:** getID3 native QuickTime/MP4 parser
- **Local input API:** `Audio::read(local MP4 path)->getMetadata(); MP4 format and AAC audio track sample rate/channels/codec`
- **Documentation:** [API reference](<https://github.com/kiwilan/php-audio/blob/684002b34e5db3fa2935d6b9ba8cba0ebd81b1a7/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp4/parsers.json) · [control verification](../../../../data/php/mp4/verification.json) · [within-ecosystem ranking](../../../../data/php/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "format": "mp4",
  "audio_sample_rate": 8000,
  "audio_channels": 1,
  "audio_codec": "ISO/IEC 14496-3 AAC"
}
```

Distinct Composer package path using getID3 QuickTime/MP4 parsing; shares the underlying getID3 family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
