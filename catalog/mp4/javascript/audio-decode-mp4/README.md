# @audio/decode-mp4 — MP4 / JavaScript

- **Pinned release:** `1.3.1`
- **Upstream:** [source repository](<https://github.com/audiojs/decode>) · [npm](<https://www.npmjs.com/package/@audio/decode-mp4>)
- **License:** MIT
- **Parsed scope:** audio_samples
- **Underlying family:** @audio/decode-mp4
- **Local input API:** `decode(Uint8Array)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@audio/decode-mp4>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "sampleRate": 8000,
  "channels": 1,
  "samples": 8000
}
```

Decodes the AAC audio track within the MP4 control.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/javascript/audio_decode_mp4/README.md)

```sh
python3 parsarium.py build mp4 javascript audio_decode_mp4
python3 parsarium.py run mp4 javascript audio_decode_mp4 controls/mp4/red-av.mp4
```
