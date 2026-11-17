# mp3agic — MP3 / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.9.1`
- **License:** MIT
- **Parser family:** mp3agic native MP3 frame and ID3v2 reader
- **Local input API:** `new Mp3File(Path.of(localFile)); getVersion(), getLayer(), getSampleRate(), getChannelMode(), getBitrate() after scanning MPEG frames`
- **Documentation:** [API reference](<https://github.com/mpatric/mp3agic/blob/master/readme.md>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [control result](../../../../data/java/mp3/verification.json)

## Observed control result

```json
{
  "codec": "MP3",
  "mpeg_version": "1.0",
  "layer": "III",
  "sample_rate": 44100,
  "channel_mode": "Mono",
  "bitrate_kbps": 64
}
```

## Run this target

```sh
python3 parsarium.py build mp3 java mp3agic
python3 parsarium.py run mp3 java mp3agic controls/mp3/tone-44k-mono.mp3
```
