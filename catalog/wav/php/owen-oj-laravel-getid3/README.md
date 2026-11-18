# owen-oj/laravel-getid3 — WAV / PHP

- **Pinned release:** `v2.6.0`
- **Upstream:** [source repository](<https://github.com/Owen-oj/laravel-getid3>) · [Packagist](<https://packagist.org/packages/owen-oj/laravel-getid3>)
- **License:** MIT
- **Parsed scope:** RIFF/WAVE PCM16 format, 8 kHz sample rate, mono channel count
- **Underlying family:** getID3 native RIFF/WAVE parser
- **Local input API:** `GetId3(local PCM WAV path)::extractInfo(); fileformat and audio sample_rate/channels/bits_per_sample`
- **Documentation:** [API reference](<https://github.com/Owen-oj/laravel-getid3/blob/6b89fc96b3dd2536fb2e53f8fee99ee6b76f9fd1/readme.md>)
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

Laravel wrapper delegates to the same pinned james-heinrich/getid3 package in its shared lock; separate package path, same parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/php/owen_oj_laravel_getid3/README.md)

```sh
python3 parsarium.py build wav php owen_oj_laravel_getid3
python3 parsarium.py run wav php owen_oj_laravel_getid3 controls/wav/256-samples.wav
```
