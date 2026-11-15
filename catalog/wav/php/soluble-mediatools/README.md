# soluble/mediatools — WAV / PHP

- **Pinned release:** `2.2.0`
- **License:** MIT
- **Parsed scope:** WAV container, 32 ms duration, PCM16 audio stream
- **Underlying family:** FFmpeg native RIFF/WAVE parser
- **Local input API:** `VideoInfoReader(FFProbeConfig)->getInfo(local PCM WAV path); format, duration and audio stream codec`
- **Documentation:** [API reference](<https://github.com/soluble-io/soluble-mediatools/blob/3c7b0cec78ee97f9a74443cb0eecf10504c1eec5/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "format": "wav",
  "duration_seconds": 0.032,
  "audio_codec": "pcm_s16le"
}
```

VideoInfoReader handles the valid WAV control and delegates to local FFprobe 9.0.2.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
