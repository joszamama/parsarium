# music-metadata — MP4 / JavaScript

- **Pinned release:** `12.4.0`
- **Upstream:** [source repository](<https://github.com/Borewit/music-metadata>) · [npm](<https://www.npmjs.com/package/music-metadata>)
- **License:** MIT
- **Parsed scope:** tracks+title
- **Underlying family:** music-metadata/ISO BMFF reader
- **Local input API:** `parseFile(path)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/music-metadata>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp4/parsers.json) · [control verification](../../../../data/javascript/mp4/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "title": "Parsarium",
  "width": 2,
  "height": 2,
  "sampleRate": 8000
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/javascript/music_metadata/README.md)

```sh
python3 parsarium.py build mp4 javascript music_metadata
python3 parsarium.py run mp4 javascript music_metadata controls/mp4/red-av.mp4
```
