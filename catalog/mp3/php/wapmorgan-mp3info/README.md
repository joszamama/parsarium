# wapmorgan/mp3info — MP3 / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.1.1`
- **License:** LGPL-3.0
- **Parser family:** Mp3Info native PHP MPEG frame-header reader (src/Mp3Info.php)
- **Local input API:** `new wapmorgan\Mp3Info\Mp3Info(local temporary file path) -> codecVersion, layerVersion, sampleRate, channel, bitRate, isVbr, audioSize, _framesCount, duration`
- **Documentation:** [API reference](<https://github.com/wapmorgan/Mp3Info/blob/e532c2e1997874f9c672c7810ce90ef15004ef94/README.md>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/php/mp3/parsers.json) · [control result](../../../../projects/mp3/php/wapmorgan_mp3info/verification.json)

## Observed control result

```json
{
  "mpeg_version": 1,
  "layer": 3,
  "sample_rate": 44100,
  "channel": "mono",
  "bitrate": 64000,
  "is_vbr": false,
  "audio_size": 2298,
  "frames": 11,
  "duration": 0.26122
}
```

## Run this target

```sh
python3 parsarium.py build mp3 php wapmorgan_mp3info
python3 parsarium.py run mp3 php wapmorgan_mp3info controls/mp3/tone-44k-mono.mp3
```
