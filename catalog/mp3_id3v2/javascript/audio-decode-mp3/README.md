# @audio/decode-mp3 — MP3 with ID3v2 / JavaScript

- **Pinned release:** `1.3.1`
- **License:** MIT
- **Parsed scope:** decoded_audio
- **Underlying family:** mpg123 WASM
- **Local input API:** `decode(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@audio/decode-mp3>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3_id3v2/parsers.json) · [control verification](../../../../data/javascript/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sampleRate": 8000,
  "channels": 2,
  "samples": 8000
}
```

Uses mpg123-decoder WASM. On this mono control the codec API yielded two PCM channels; only sample rate and sample count establish acceptance of the tagged MP3.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/javascript/audio_decode_mp3/README.md)

```sh
python3 parsarium.py build mp3_id3v2 javascript audio_decode_mp3
python3 parsarium.py run mp3_id3v2 javascript audio_decode_mp3 controls/mp3_id3v2/tone-tags.mp3
```
