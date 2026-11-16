# php-ffmpeg/php-ffmpeg — ASCII PNM / PHP

- **Pinned release:** `v1.4.0`
- **License:** MIT
- **Parsed scope:** identified PPM codec and decoded dimensions
- **Underlying family:** FFmpeg PPM decoder
- **Local input API:** `FFProbe::create()->streams(local P3 file)->videos()->first(); codec_name, width, height`
- **Documentation:** [API reference](<https://github.com/PHP-FFMpeg/PHP-FFMpeg/blob/41fa00949ea2758cd34f076a8030df7198d57759/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_pnm/parsers.json) · [control verification](../../../../data/php/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "codec": "ppm",
  "width": 2,
  "height": 1
}
```

FFProbe delegates ASCII P3 probing to the installed FFmpeg PPM decoder. This is one package path into a distinct FFmpeg parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/php/php_ffmpeg_php_ffmpeg/README.md)

```sh
python3 parsarium.py build ascii_pnm php php_ffmpeg_php_ffmpeg
python3 parsarium.py run ascii_pnm php php_ffmpeg_php_ffmpeg controls/ascii_pnm/red-green.ppm
```
