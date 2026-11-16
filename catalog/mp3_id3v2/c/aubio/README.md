# aubio — MP3 with ID3v2 / C

- **Pinned release:** `0.4.9`
- **License:** GPL-3.0-or-later
- **Parsed scope:** MP3 audio stream fields and 256 decoded samples from tagged local file; tag text is not exposed
- **Underlying family:** aubio source frontend over Apple AudioToolbox or libsndfile
- **Local input API:** `new_aubio_source(local filename, native sample rate, 256); aubio_source_do; aubio_source_get_samplerate/get_channels`
- **Documentation:** [API reference](<https://aubio.org/doc/latest/io_2test-source_8c-example.html>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3_id3v2/parsers.json) · [control verification](../../../../data/c/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "decoded_samples": 256
}
```

Pinned source.c tries Apple AudioToolbox before libsndfile on this macOS build, and installed libaubio links both. The adapter does not reveal which backend succeeded; exact underlying decoder family remains unresolved. C and C++ share one aubio C implementation.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp3_id3v2/c/aubio/README.md)

```sh
python3 parsarium.py build mp3_id3v2 c aubio
python3 parsarium.py run mp3_id3v2 c aubio controls/mp3_id3v2/tone-tags.mp3
```
