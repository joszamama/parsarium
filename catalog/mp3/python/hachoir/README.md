# hachoir — MP3 / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.4.0`
- **License:** GPL-2.0-only
- **Parser family:** hachoir mpeg_audio parser
- **Local input API:** `hachoir.parser.audio.mpeg_audio.MpegAudioFile(hachoir.stream.FileInputStream(io.BytesIO(local bytes)), validate=True)['frames'] -> frame[] field sets`
- **Documentation:** [API reference](<https://github.com/vstinner/hachoir/blob/3.4.0/doc/developer.rst>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/python/mp3/parsers.json) · [control result](../../../../projects/mp3/python/hachoir/verification.json)

## Observed control result

```json
{
  "version": "1",
  "layer": "III",
  "sample_rate": 44100,
  "bitrate": 64000,
  "channel_mode": "Single channel",
  "channels": 1,
  "frames": 11,
  "frame_bytes": 2298
}
```

## Run this target

```sh
python3 parsarium.py build mp3 python hachoir
python3 parsarium.py run mp3 python hachoir controls/mp3/tone-44k-mono.mp3
```
