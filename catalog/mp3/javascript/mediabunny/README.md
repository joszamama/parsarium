# mediabunny — MP3 / JavaScript

- **Pinned release:** `1.66.0`
- **Upstream:** [source repository](<https://github.com/Vanilagy/mediabunny>) · [npm](<https://www.npmjs.com/package/mediabunny>)
- **License:** MPL-2.0
- **Parsed scope:** Every MPEG Layer III frame of an untagged stream from local bytes, demuxed by mediabunny's own frame-header reader: format, codec, sample rate, channels, frame count, frame bytes, samples per channel (from duration); no audio decode
- **Underlying family:** mediabunny TypeScript MP3 demuxer
- **Local input API:** `new Input({ source: new BufferSource(bytes), formats: ALL_FORMATS }); getFormat(); getPrimaryAudioTrack(); new EncodedPacketSink(track).packets(); track.computeDuration()`
- **Documentation:** [API reference](<https://mediabunny.dev/guide/reading-media-files>)
- **Catalog evidence:** [parser record](../../../../data/javascript/mp3/parsers.json) · [control verification](../../../../data/javascript/mp3/verification.json) · [within-ecosystem ranking](../../../../data/javascript/mp3/ranking.md)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)

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

Own frame-header reader (dist/modules/src/mp3/mp3-reader.js, mp3-demuxer.js). Not one of the ten JavaScript paths selected in the former MP3-with-ID3v2 cell; that cell's music-metadata path is a separate MPEG frame parser and its @audio/decode paths use mpg123 WASM. mediabunny also has an ID3 reader (id3.js) that the untagged controls do not exercise.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3/javascript/mediabunny/README.md)

```sh
python3 parsarium.py build mp3 javascript mediabunny
python3 parsarium.py run mp3 javascript mediabunny controls/mp3/tone-44k-mono.mp3
```

**Coverage limit:** Untagged MPEG Layer III only; two valid CBR controls do not establish VBR, Xing/Info, free-format, Layer I/II, or MPEG-2.5 support. mediabunny demuxes frames and reads headers; it does not decode MP3 audio without WebCodecs, which this path does not use.
