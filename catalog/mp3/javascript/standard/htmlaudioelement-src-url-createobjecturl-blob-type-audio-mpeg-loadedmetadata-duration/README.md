# HTMLAudioElement.src = URL.createObjectURL(Blob({type:audio/mpeg})); loadedmetadata; duration — MP3 / JavaScript

- **Runtime:** Chromium 153.0.8010.12 via Playwright 1.63.0
- **Input API:** `HTMLAudioElement.src = URL.createObjectURL(Blob({type:audio/mpeg})); loadedmetadata; duration`
- **Official documentation:** [reference](https://html.spec.whatwg.org/multipage/media.html#the-audio-element)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../../controls/mp3/id3v2-tagged-tone.mp3)
- **Inventory and verification:** [standard API record](../../../../../data/javascript/mp3/standard.json) · [saved result](../../../../../data/javascript/mp3/verification.json)

## Observed control result

```json
{
  "duration": 1
}
```

[Control adapter](../../../../../adapters/javascript/mp3_browser.mjs)

## Run the valid control

[Browser container and control receipt](../../../../../projects/mp3/javascript/stdlib_browser_audio_metadata/README.md)

```sh
python3 projects/mp3/javascript/stdlib_browser_audio_metadata/verify-control.py
```

The browser runs this control, but its native parser source coverage and AFL++ parser feedback are unavailable. This path remains staged.
