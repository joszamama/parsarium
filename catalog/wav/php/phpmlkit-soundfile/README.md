# phpmlkit/soundfile — WAV / PHP

- **Pinned release:** `1.2.0`
- **License:** MIT
- **Parsed scope:** WAV container, PCM16 subtype, 8 kHz mono signal
- **Underlying family:** libsndfile native RIFF/WAVE parser
- **Local input API:** `sf_info(local PCM WAV path); sampleRate, channels, AudioFormat::Wav and SampleFormat::Pcm16`
- **Documentation:** [API reference](<https://github.com/phpmlkit/soundfile/blob/acf88e283d9175c1eeca3670a74807fb345a9198/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "format": "Wav",
  "subtype": "Pcm16"
}
```

PHP FFI binding to package-distributed libsndfile 1.2.2. Same release lock as the PHP MP3 cell.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
