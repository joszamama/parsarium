# indiehd/audio-manipulator — WAV / PHP

- **Pinned release:** `v4.1.0`
- **Upstream:** [source repository](<https://github.com/indiehd/audio-manipulator>) · [Packagist](<https://packagist.org/packages/indiehd/audio-manipulator>)
- **License:** MIT
- **Parsed scope:** RIFF/WAVE PCM16 format, 8 kHz sample rate, mono channel count
- **Underlying family:** getID3 native RIFF/WAVE parser
- **Local input API:** `MediaParser::analyze(local PCM WAV path); fileformat and audio sample rate/channels/bit depth`
- **Documentation:** [API reference](<https://github.com/indiehd/audio-manipulator/blob/1e2f6d76030200c77cd727b40d3ea6166957f45d/src/MediaParsing/MediaParserInterface.php>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "fileformat": "wav",
  "sample_rate": 8000,
  "channels": 1,
  "bits_per_sample": 16
}
```

Public MediaParserInterface accepts a local file path; implementation delegates to pinned getID3.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/php/indiehd_audio_manipulator/README.md)

```sh
python3 parsarium.py build wav php indiehd_audio_manipulator
python3 parsarium.py run wav php indiehd_audio_manipulator controls/wav/256-samples.wav
```
