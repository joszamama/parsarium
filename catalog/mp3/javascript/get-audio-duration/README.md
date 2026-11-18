# get-audio-duration — MP3 / JavaScript

- **Pinned release:** `4.0.1`
- **Upstream:** [source repository](<https://github.com/caffco/get-audio-duration>) · [npm](<https://www.npmjs.com/package/get-audio-duration>)
- **License:** MIT
- **Parsed scope:** duration
- **Underlying family:** FFprobe wrapper
- **Local input API:** `getAudioDurationInSeconds(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/get-audio-duration>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3/parsers.json) · [control verification](../../../../data/javascript/mp3/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "duration_ms": 1152
}
```

Invokes pinned @ffprobe-installer/ffprobe; duration includes encoder padding.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/javascript/get_audio_duration/README.md)

```sh
python3 parsarium.py build mp3 javascript get_audio_duration
python3 parsarium.py run mp3 javascript get_audio_duration controls/mp3/id3v2-tagged-tone.mp3
```
