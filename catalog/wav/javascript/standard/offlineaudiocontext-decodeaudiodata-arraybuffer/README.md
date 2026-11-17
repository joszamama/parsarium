# OfflineAudioContext.decodeAudioData(ArrayBuffer) — WAV / JavaScript

- **Runtime:** Chromium 153.0.8010.12 via Playwright 1.63.0
- **Input API:** `OfflineAudioContext.decodeAudioData(ArrayBuffer)`
- **Official documentation:** [reference](https://www.w3.org/TR/webaudio-1.1/#dom-baseaudiocontext-decodeaudiodata)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../../controls/wav/four-samples.wav)
- **Inventory and verification:** [standard API record](../../../../../data/javascript/wav/standard.json) · [saved result](../../../../../data/javascript/wav/verification.json)

## Observed control result

```json
{
  "sampleRate": 8000,
  "channels": 1,
  "sampleCount": 4,
  "sampleSigns": [
    0,
    1,
    -1,
    0
  ]
}
```

[Control adapter](../../../../../adapters/javascript/wav_browser.mjs)

## Run the valid control

[Browser container and control receipt](../../../../../projects/wav/javascript/stdlib_browser_decodeaudiodata/README.md)

```sh
python3 projects/wav/javascript/stdlib_browser_decodeaudiodata/verify-control.py
```

The browser runs this control, but its native parser source coverage and AFL++ parser feedback are unavailable. This path remains staged.
