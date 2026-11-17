# mediabunny — MP3 / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.66.0`
- **License:** MPL-2.0
- **Parser family:** mediabunny TypeScript MP3 demuxer
- **Local input API:** `new Input({ source: new BufferSource(bytes), formats: ALL_FORMATS }); getFormat(); getPrimaryAudioTrack(); new EncodedPacketSink(track).packets(); track.computeDuration()`
- **Documentation:** [API reference](<https://mediabunny.dev/guide/reading-media-files>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3/parsers.json) · [control result](../../../../projects/mp3/javascript/mediabunny/verification.json)

## Observed control result

```json
{
  "format": "MP3",
  "codec": "mp3",
  "sample_rate": 44100,
  "channels": 1,
  "frames": 11,
  "frame_bytes": 2298,
  "samples_per_channel": 12672
}
```

## Run this target

```sh
python3 parsarium.py build mp3 javascript mediabunny
python3 parsarium.py run mp3 javascript mediabunny controls/mp3/tone-44k-mono.mp3
```
