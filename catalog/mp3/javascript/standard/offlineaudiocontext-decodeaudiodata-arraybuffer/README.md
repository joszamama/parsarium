# OfflineAudioContext.decodeAudioData(ArrayBuffer) — MP3 / JavaScript

- **Runtime:** Chromium 153.0.8010.12 via Playwright 1.63.0
- **Input API:** `OfflineAudioContext.decodeAudioData(ArrayBuffer)`
- **Official documentation:** [reference](https://www.w3.org/TR/webaudio-1.1/#dom-baseaudiocontext-decodeaudiodata)
- **Valid control:** [`controls/mp3/id3v2-tagged-tone.mp3`](../../../../../controls/mp3/id3v2-tagged-tone.mp3)
- **Inventory and verification:** [standard API record](../../../../../data/javascript/mp3/standard.json) · [saved result](../../../../../data/javascript/mp3/verification.json)

## Observed control result

```json
{
  "sampleRate": 8000,
  "channels": 1,
  "samples": 8000
}
```

[Control adapter](../../../../../adapters/javascript/mp3_browser.mjs)

## Run the valid control

[Browser container and control receipt](../../../../../projects/mp3/javascript/stdlib_browser_decodeaudiodata/README.md)

```sh
python3 projects/mp3/javascript/stdlib_browser_decodeaudiodata/verify-control.py
```

The browser runs this control, but its native parser source coverage and AFL++ parser feedback are unavailable. This path remains staged.
