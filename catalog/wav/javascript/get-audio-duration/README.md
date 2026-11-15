# get-audio-duration — WAV / JavaScript

- **Pinned release:** `4.0.1`
- **License:** MIT
- **Parsed scope:** duration
- **Underlying family:** ffprobe
- **Local input API:** `getAudioDurationInSeconds(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/get-audio-duration>)
- **Catalog evidence:** [parser record](../../../../data/javascript/wav/parsers.json) · [control verification](../../../../data/javascript/wav/verification.json) · [within-ecosystem ranking](../../../../data/javascript/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "durationSeconds": 0.0005
}
```

Local wrapper invoking the bundled ffprobe executable; its output is not an independent parser implementation.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
