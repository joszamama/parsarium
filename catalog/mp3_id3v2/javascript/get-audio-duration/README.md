# get-audio-duration — MP3 with ID3v2 / JavaScript

- **Pinned release:** `4.0.1`
- **License:** MIT
- **Parsed scope:** duration
- **Underlying family:** FFprobe wrapper
- **Local input API:** `getAudioDurationInSeconds(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/get-audio-duration>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3_id3v2/parsers.json) · [control verification](../../../../data/javascript/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "duration_ms": 1152
}
```

Invokes pinned @ffprobe-installer/ffprobe; duration includes encoder padding.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/javascript/get_audio_duration/README.md)

```sh
python3 parsarium.py build mp3_id3v2 javascript get_audio_duration
python3 parsarium.py run mp3_id3v2 javascript get_audio_duration controls/mp3_id3v2/tone-tags.mp3
```
