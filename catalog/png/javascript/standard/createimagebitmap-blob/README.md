# createImageBitmap(Blob) — PNG / JavaScript

- **Runtime:** Chromium browser via Playwright 1.63.0
- **Input API:** `createImageBitmap(Blob)`
- **Official documentation:** [reference](https://html.spec.whatwg.org/multipage/imagebitmap-and-animations.html#dom-createimagebitmap-dev)
- **Valid control:** [`controls/png/red-green.png`](../../../../../controls/png/red-green.png)
- **Inventory and verification:** [standard API record](../../../../../data/javascript/png/standard.json) · [saved result](../../../../../data/javascript/png/verification.json)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgba": [
    255,
    0,
    0,
    255,
    0,
    255,
    0,
    255
  ]
}
```

[Control adapter](../../../../../adapters/javascript/png_browser.mjs)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
