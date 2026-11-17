# music-metadata — MP3 / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `12.5.0`
- **License:** MIT
- **Parser family:** music-metadata JavaScript MPEG frame parser
- **Local input API:** `parseBuffer(Uint8Array, { mimeType: 'audio/mpeg', size }, { duration: true }) -> IAudioMetadata.format (codec, sampleRate, numberOfChannels, bitrate, codecProfile, numberOfSamples, duration); parseFile(path) and parseStream(Readable, { mimeType: 'audio/mpeg' }) checked equal by api-check.js`
- **Documentation:** [API reference](<https://github.com/Borewit/music-metadata#readme>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3/parsers.json) · [control result](../../../../projects/mp3/javascript/music_metadata/verification.json)

## Observed control result

```json
{
  "container": "MPEG",
  "codec": "MPEG 1 Layer 3",
  "mpeg_version": 1,
  "layer": 3,
  "codec_profile": "CBR",
  "sample_rate": 44100,
  "channels": 1,
  "bitrate": 64000,
  "number_of_samples": 12672,
  "duration": 0.2873469387755102,
  "tag_types": [],
  "warnings": 0
}
```

## Run this target

```sh
python3 parsarium.py build mp3 javascript music_metadata
python3 parsarium.py run mp3 javascript music_metadata controls/mp3/tone-44k-mono.mp3
```
