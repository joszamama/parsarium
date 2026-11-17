# james-heinrich/getid3 — MP3 / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.9.28`
- **License:** GPL-1.0-or-later OR LGPL-3.0-only OR MPL-2.0
- **Parser family:** getID3 native MP3 frame parser (module.audio.mp3.php)
- **Local input API:** `(new getID3())->analyze(local temporary file path) -> ['mpeg']['audio'] frame-header fields, ['playtime_seconds'], ['avdataoffset'..'avdataend']`
- **Documentation:** [API reference](<https://github.com/JamesHeinrich/getID3/blob/v1.9.28/README.md>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/php/mp3/parsers.json) · [control result](../../../../projects/mp3/php/getid3/verification.json)

## Observed control result

```json
{
  "mpeg_version": "1",
  "layer": 3,
  "sample_rate": 44100,
  "channels": 1,
  "channelmode": "mono",
  "bitrate": 64000,
  "bitrate_mode": "cbr",
  "framelength": 208,
  "playtime_seconds": 0.28725,
  "audio_data_bytes": 2298,
  "tag_formats": []
}
```

## Run this target

```sh
python3 parsarium.py build mp3 php getid3
python3 parsarium.py run mp3 php getid3 controls/mp3/tone-44k-mono.mp3
```
