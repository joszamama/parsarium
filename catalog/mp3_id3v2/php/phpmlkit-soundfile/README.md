# phpmlkit/soundfile — MP3 with ID3v2 / PHP

- **Pinned release:** `1.2.0`
- **License:** MIT
- **Parsed scope:** ID3v2.3 title, artist, album plus MPEG Layer III format and 8 kHz sample rate
- **Underlying family:** libsndfile native MP3 and ID3 parser
- **Local input API:** `sf_info(local tagged MP3 path) and sf_metadata(local tagged MP3 path); MPEG Layer III signal properties and title/artist/album`
- **Documentation:** [API reference](<https://github.com/phpmlkit/soundfile/blob/acf88e283d9175c1eeca3670a74807fb345a9198/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp3_id3v2/parsers.json) · [control verification](../../../../data/php/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/php/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot",
  "sample_rate": 8000,
  "format": "Mpeg",
  "subtype": "MpegLayerIII"
}
```

PHP FFI binding to the package-distributed libsndfile 1.2.2 library. The platform installer plugin was disabled; the pinned distribution contains the darwin-arm64 native binary used in this run.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/php/phpmlkit_soundfile/README.md)

```sh
python3 parsarium.py build mp3_id3v2 php phpmlkit_soundfile
python3 parsarium.py run mp3_id3v2 php phpmlkit_soundfile controls/mp3_id3v2/tone-tags.mp3
```
