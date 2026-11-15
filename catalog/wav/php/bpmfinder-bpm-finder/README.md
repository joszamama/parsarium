# bpmfinder/bpm-finder — WAV / PHP

- **Pinned release:** `v0.1.0`
- **License:** MIT
- **Parsed scope:** PCM16 WAV header and 120 BPM pulse train, 8 kHz mono, 4 seconds
- **Underlying family:** BpmFinder native PHP PCM WAV decoder
- **Local input API:** `AudioFileBpmAnalyzer::analyzeFile(local rhythmic PCM WAV path); format, sample rate, channels, duration and BPM`
- **Documentation:** [API reference](<https://github.com/wsgtcyx/bpm-finder-Packagist/blob/42a2792408844170f6f14920c945bfa1eaabfa11/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/120-bpm-clicks.wav`](../../../../controls/wav/120-bpm-clicks.wav)

## Observed control result

```json
{
  "format": "wav",
  "sample_rate": 8000,
  "channels": 1,
  "duration_seconds": 4,
  "bpm": 120
}
```

Package WavAudioDecoder reads RIFF chunks and PCM samples directly; BPM analysis uses the decoded samples.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
