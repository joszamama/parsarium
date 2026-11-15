# HTMLAudioElement.src = URL.createObjectURL(Blob({type:audio/mpeg})); loadedmetadata; duration — MP3 with ID3v2 / JavaScript

- **Runtime:** Chromium 153.0.8010.12 via Playwright 1.63.0
- **Input API:** `HTMLAudioElement.src = URL.createObjectURL(Blob({type:audio/mpeg})); loadedmetadata; duration`
- **Official documentation:** [reference](https://html.spec.whatwg.org/multipage/media.html#the-audio-element)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../../controls/mp3_id3v2/tone-tags.mp3)
- **Inventory and verification:** [standard API record](../../../../../data/javascript/mp3_id3v2/standard.json) · [saved result](../../../../../data/javascript/mp3_id3v2/verification.json)

## Observed control result

Loaded local tagged MP3 and reported one-second duration

[Control adapter](../../../../../adapters/javascript/mp3_id3v2_browser.mjs)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
