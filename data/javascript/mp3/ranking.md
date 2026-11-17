# JAVASCRIPT × MP3: selected parsers

10 control-verified third-party paths selected from 13 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

npm registry tarball downloads.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [mediabunny](https://mediabunny.dev/guide/reading-media-files) | 1.66.0 | 26,071,768 | Every MPEG Layer III frame of an untagged stream from local bytes, demuxed by mediabunny's own frame-header reader: format, codec, sample rate, channels, frame count, frame bytes, samples per channel (from duration); no audio decode | mediabunny TypeScript MP3 demuxer |
| 2 | [music-metadata](https://www.npmjs.com/package/music-metadata) | 12.4.0 | 9,827,896 | tags+audio_header | music-metadata |
| 3 | [codec-parser](https://github.com/eshaz/codec-parser#readme) | 2.5.0 | 2,683,215 | Every MPEG Layer III frame of an untagged stream from a local Uint8Array, split by codec-parser's own frame-header parser: codec, layer, sample rate, channels, header-table bitrate, frame count, frame bytes, samples per frame, total samples, distinct header variants; no audio decode | codec-parser JavaScript MPEG frame parser |
| 4 | [@audio/decode-mp3](https://www.npmjs.com/package/@audio/decode-mp3) | 1.3.1 | 703,988 | decoded_audio | mpg123 WASM |
| 5 | [mediainfo.js](https://www.npmjs.com/package/mediainfo.js) | 0.3.8 | 650,653 | tags | MediaInfoLib WASM |
| 6 | [@audio/decode](https://www.npmjs.com/package/@audio/decode) | 4.3.0 | 621,561 | decoded_audio | mpg123 WASM |
| 7 | [get-audio-duration](https://www.npmjs.com/package/get-audio-duration) | 4.0.1 | 206,806 | duration | FFprobe wrapper |
| 8 | [node-id3](https://www.npmjs.com/package/node-id3) | 0.2.9 | 145,214 | tags | node-id3 |
| 9 | [id3js](https://www.npmjs.com/package/id3js) | 2.1.1 | 62,319 | tags+version | id3js |
| 10 | [mp3-duration](https://www.npmjs.com/package/mp3-duration) | 1.1.0 | 43,261 | duration | mp3-duration |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
