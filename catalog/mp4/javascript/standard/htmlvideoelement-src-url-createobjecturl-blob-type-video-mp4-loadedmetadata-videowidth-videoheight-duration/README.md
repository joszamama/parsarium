# HTMLVideoElement.src = URL.createObjectURL(Blob({type:video/mp4})); loadedmetadata; videoWidth/videoHeight/duration — MP4 / JavaScript

- **Runtime:** Chromium 153.0.8010.12 via Playwright 1.63.0
- **Input API:** `HTMLVideoElement.src = URL.createObjectURL(Blob({type:video/mp4})); loadedmetadata; videoWidth/videoHeight/duration`
- **Official documentation:** [reference](https://html.spec.whatwg.org/multipage/media.html#the-video-element)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../../controls/mp4/red-av.mp4)
- **Inventory and verification:** [standard API record](../../../../../data/javascript/mp4/standard.json) · [saved result](../../../../../data/javascript/mp4/verification.json)

## Observed control result

```json
{
  "width": 2,
  "height": 2,
  "duration": 1
}
```

[Control adapter](../../../../../adapters/javascript/mp4_browser.mjs)

## Run the valid control

[Browser container and control receipt](../../../../../projects/mp4/javascript/stdlib_browser_video_metadata/README.md)

```sh
python3 projects/mp4/javascript/stdlib_browser_video_metadata/verify-control.py
```

The browser runs this control, but its native parser source coverage and AFL++ parser feedback are unavailable. This path remains staged.
