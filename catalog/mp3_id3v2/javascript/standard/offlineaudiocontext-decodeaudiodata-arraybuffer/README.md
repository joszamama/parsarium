# OfflineAudioContext.decodeAudioData(ArrayBuffer) — MP3 with ID3v2 / JavaScript

- **Runtime:** Chromium 153.0.8010.12 via Playwright 1.63.0
- **Input API:** `OfflineAudioContext.decodeAudioData(ArrayBuffer)`
- **Official documentation:** [reference](https://www.w3.org/TR/webaudio-1.1/#dom-baseaudiocontext-decodeaudiodata)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../../controls/mp3_id3v2/tone-tags.mp3)
- **Inventory and verification:** [standard API record](../../../../../data/javascript/mp3_id3v2/standard.json) · [saved result](../../../../../data/javascript/mp3_id3v2/verification.json)

## Observed control result

```json
{
  "sampleRate": 8000,
  "channels": 1,
  "samples": 8000
}
```

[Control adapter](../../../../../adapters/javascript/mp3_id3v2_browser.mjs)

## Run the valid control

[Browser container and control receipt](../../../../../projects/mp3_id3v2/javascript/stdlib_browser_decodeaudiodata/README.md)

```sh
python3 projects/mp3_id3v2/javascript/stdlib_browser_decodeaudiodata/verify-control.py
```

The browser runs this control, but its native parser source coverage and AFL++ parser feedback are unavailable. This path remains staged.
