# duncan3dc/meta-audio — MP3 with ID3v2 / PHP

- **Pinned release:** `0.6.0`
- **License:** Apache-2.0
- **Parsed scope:** ID3v2.4 title, artist, and album
- **Underlying family:** duncan3dc MetaAudio native ID3 parser
- **Local input API:** `Tagger::addDefaultModules(); Tagger::open(local tagged MP3 path); getTitle/getArtist/getAlbum`
- **Documentation:** [API reference](<https://github.com/duncan3dc/meta-audio/blob/350b2f9f23dcf00dfb854e3d99634919cd74360b/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/mp3_id3v2/parsers.json) · [control verification](../../../../data/php/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/php/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags-v24.mp3`](../../../../controls/mp3_id3v2/tone-tags-v24.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "artist": "Control",
  "album": "Pilot"
}
```

Own PHP ID3v2 module; the documented default-module setup is required. The ID3v2.4 control uses synchsafe frame sizes.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/php/duncan3dc_meta_audio/README.md)

```sh
python3 parsarium.py build mp3_id3v2 php duncan3dc_meta_audio
python3 parsarium.py run mp3_id3v2 php duncan3dc_meta_audio controls/mp3_id3v2/tone-tags-v24.mp3
```
