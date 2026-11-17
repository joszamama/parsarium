# mp3spi — MP3 / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.9.5.4`
- **License:** LGPL-2.0-or-later
- **Parser family:** JavaZoom JLayer via MP3SPI Java Sound provider and soundlibs JLayer fork
- **Local input API:** `new MpegAudioFileReader().getAudioInputStream(BufferedInputStream(ByteArrayInputStream(local bytes))); new MpegFormatConversionProvider().getAudioInputStream(PCM_SIGNED, encoded); read all decoded PCM samples`
- **Documentation:** [API reference](<https://docs.oracle.com/en/java/javase/25/docs/api/java.desktop/javax/sound/sampled/spi/AudioFileReader.html>)
- **Valid control:** [`controls/mp3/tone-44k-mono.mp3`](../../../../controls/mp3/tone-44k-mono.mp3)
- **Catalog evidence:** [parser record](../../../../data/java/mp3/parsers.json) · [control result](../../../../data/java/mp3/verification.json)

## Observed control result

```json
{
  "codec": "MP3",
  "sample_rate": 44100,
  "channels": 1,
  "frames": 11,
  "decoded_samples": 12672
}
```

## Run this target

```sh
python3 parsarium.py build mp3 java mp3spi
python3 parsarium.py run mp3 java mp3spi controls/mp3/tone-44k-mono.mp3
```
