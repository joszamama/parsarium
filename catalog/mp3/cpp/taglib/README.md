# taglib — MP3 / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.3.2`
- **License:** LGPL-2.1-only OR MPL-1.1
- **Parser family:** TagLib MPEG frame-header and tag parser
- **Local input API:** `TagLib::ByteVectorStream(local bytes); TagLib::MPEG::File(IOStream*, readProperties=true, AudioProperties::Accurate); audioProperties()->version()/layer()/sampleRate()/channels()/bitrate()/lengthInMilliseconds()`
- **Documentation:** [API reference](<https://taglib.org/api/classTagLib_1_1MPEG_1_1File.html>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp3/parsers.json) · [control result](../../../../projects/mp3/cpp/taglib/verification.json)

## Observed control result

```json
{
  "version": 1,
  "layer": 3,
  "sample_rate": 44100,
  "channels": 1,
  "bitrate_kbps": 64,
  "length_ms": 287
}
```

## Run this target

```sh
python3 parsarium.py build mp3 cpp taglib
python3 parsarium.py run mp3 cpp taglib controls/mp3/tone-44k-mono.mp3
```
