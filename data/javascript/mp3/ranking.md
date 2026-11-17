# JAVASCRIPT × MP3: selected parsers (pilot)

2 control-verified third-party paths selected. The ceiling is ten; this pilot builds leads whose own code parses untagged MPEG Layer III frame headers from a documented local byte API, and does not pad the selection. music-metadata ranks between the two selected paths and is not built, so they are not the top two by downloads. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

npm downloads over 2026-10-17 to 2026-11-15 (30 days), observed 2026-11-17T03:43:56Z ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [mediabunny](https://mediabunny.dev/guide/reading-media-files) | 1.66.0 | 26,071,768 | Every Layer III frame of an untagged stream from a `BufferSource`: format, codec, sample rate, channels, frame count, frame bytes, samples per channel; no audio decode | mediabunny TypeScript MP3 demuxer |
| 2 | [codec-parser](https://github.com/eshaz/codec-parser#readme) | 2.5.0 | 2,683,215 | Every Layer III frame of an untagged stream from a `Uint8Array` via `parseAll`: layer, sample rate, channels, header bitrate, frame count, frame bytes, samples per frame, total samples; no audio decode | codec-parser JavaScript MPEG frame parser |

Both paths match the independent frame-header walker in `controls/mp3/check_controls.py` on both untagged controls and frame every input byte.

## Standard API (unranked)

None. The Node.js 26.10.0 API docs have no MPEG audio parser or decoder; `Buffer` and `fs` move bytes only. Browser Web Audio `decodeAudioData` is recorded under mp3_id3v2 and is not a Node API.

## Parser family relative to mp3_id3v2

Neither mediabunny nor codec-parser is one of the ten mp3_id3v2/javascript paths. They are separate families: different authors and repositories, and codec-parser 2.5.0 has no runtime dependencies. The music-metadata path counted there has its own MPEG frame parser and is the highest-download unbuilt lead here; the mpg123 WASM wrappers share the libmpg123 family with the C plain MP3 pilot.

## Lead log

Numeric leads from the same snapshot, not verified and not selected.

| Lead | Version seen | Downloads (30 days) | Kind | Reason |
| --- | --- | ---: | --- | --- |
| [music-metadata](https://www.npmjs.com/package/music-metadata) | 12.5.0 | 9,827,896 | own parser not selected | Own MPEG frame-header parser (lib/mpeg/MpegParser.js) behind documented parseBuffer/parseFile/parseStream; reports sampleRate, numberOfChannels, codec and frame-scanned duration. Fewer downloads than mediabunny, so not built here. Same music-metadata parser family as the verified mp3_id3v2/javascript path (12.4.0 there). |
| [mpg123-decoder](https://www.npmjs.com/package/mpg123-decoder) | 1.0.3 | 2,505,430 | decoder not selected | mpg123 compiled to WASM with documented MPEGDecoder.decode(Uint8Array). Same libmpg123 engine as the verified C plain MP3 pilot and the mp3_id3v2/javascript @audio/decode paths. |
| [audio-decode](https://www.npmjs.com/package/audio-decode) | 3.12.0 | 1,467,199 | wrapper | Unscoped alias of @audio/decode; MP3 path delegates to @audio/decode-mp3 and mpg123-decoder WASM (libmpg123 family). |
| [@audio/decode-mp3](https://www.npmjs.com/package/@audio/decode-mp3) | 1.3.1 | 703,988 | wrapper | Delegates MP3 decoding to mpg123-decoder WASM (libmpg123 family); verified in mp3_id3v2/javascript for the tagged control. |
| [@audio/decode](https://www.npmjs.com/package/@audio/decode) | 4.3.0 | 621,561 | wrapper | Facade over @audio/decode-mp3 and mpg123-decoder WASM (libmpg123 family); verified in mp3_id3v2/javascript. |
| [mp3-duration](https://www.npmjs.com/package/mp3-duration) | 1.1.0 | 43,261 | duration only | Own frame-header scan that returns only a duration number; no frame metadata API. Verified in mp3_id3v2/javascript for duration scope. |
| [get-mp3-duration](https://www.npmjs.com/package/get-mp3-duration) | 1.0.0 | 41,334 | duration only | Own frame-header scan that returns only milliseconds from a Buffer; verified in mp3_id3v2/javascript for duration scope. |
| [mp3-parser](https://www.npmjs.com/package/mp3-parser) | 0.3.0 | 40,519 | own parser not selected | Own frame and tag reader (readFrameHeader, readFrame over DataView); low downloads relative to mediabunny. Not run. |
| [is-mp3](https://www.npmjs.com/package/is-mp3) | 1.1.4 | 39,703 | signature only | Signature check on leading bytes; does not parse frame streams. |
| [mp3](https://www.npmjs.com/package/mp3) | 0.1.0 | 26,941 | decoder not selected | Aurora.js Layer III decoder plugin; requires the Aurora.js framework; low downloads. Not run. |
| [js-mp3](https://www.npmjs.com/package/js-mp3) | 0.1.0 | 8,396 | decoder not selected | Pure JavaScript decoder; low downloads. Not run. |
| [minimp3](https://www.npmjs.com/package/minimp3) | 2.0.0 | 184 | decoder not selected | Native Node bindings for minimp3 (C); low downloads. Not run. |
| [mpeg-frame-parser](https://www.npmjs.com/package/mpeg-frame-parser) | 0.3.1 | 23 | own parser not selected | Small MPEG audio frame metadata stream; negligible downloads. Not run. |

Queries: `mp3 parser`, `mpeg audio`, `mp3 decoder`, `mp3 frame`, `mp3 duration`, `mp3 demuxer`; limit 100 each; 600 hits, 465 unique. Downloads were fetched for 15 hand-picked candidates, not every hit.
