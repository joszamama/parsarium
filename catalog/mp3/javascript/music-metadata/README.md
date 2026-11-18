# music-metadata — MP3 / JavaScript

- **Pinned release:** `12.4.0`
- **Upstream:** [source repository](<https://github.com/Borewit/music-metadata>) · [npm](<https://www.npmjs.com/package/music-metadata>)
- **License:** MIT
- **Parsed scope:** tags+audio_header
- **Underlying family:** music-metadata
- **Local input API:** `parseFile(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/music-metadata>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3/parsers.json) · [control verification](../../../../data/javascript/mp3/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3/ranking.md)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../controls/mp3/id3v2-tagged-tone.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot",
  "sampleRate": 8000
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/javascript/music_metadata/README.md)

```sh
python3 parsarium.py build mp3 javascript music_metadata
python3 parsarium.py run mp3 javascript music_metadata controls/mp3/id3v2-tagged-tone.mp3
```
