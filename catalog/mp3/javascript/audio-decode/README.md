# @audio/decode — MP3 / JavaScript

- **Pinned release:** `4.3.0`
- **Upstream:** [source repository](<https://github.com/audiojs/decode>) · [npm](<https://www.npmjs.com/package/@audio/decode>)
- **License:** MIT
- **Parsed scope:** decoded_audio
- **Underlying family:** mpg123 WASM
- **Local input API:** `decode(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@audio/decode>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3/parsers.json) · [control verification](../../../../data/javascript/mp3/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "sampleRate": 8000,
  "channels": 1,
  "samples": 8000
}
```

Facade delegates MP3 decoding to @audio/decode-mp3 and mpg123-decoder WASM.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/javascript/audio_decode/README.md)

```sh
python3 parsarium.py build mp3 javascript audio_decode
python3 parsarium.py run mp3 javascript audio_decode controls/mp3/id3v2-tagged-tone.mp3
```
