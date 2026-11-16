# HTMLImageElement.src = URL.createObjectURL(Blob({type:'image/svg+xml'})); decode(); canvas.drawImage() — SVG / JavaScript

- **Runtime:** Chromium 153.0.8010.12 via Playwright 1.63.0
- **Input API:** `HTMLImageElement.src = URL.createObjectURL(Blob({type:'image/svg+xml'})); decode(); canvas.drawImage()`
- **Official documentation:** [reference](https://html.spec.whatwg.org/multipage/embedded-content.html#the-img-element)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../../controls/svg/red-green.svg)
- **Inventory and verification:** [standard API record](../../../../../data/javascript/svg/standard.json) · [saved result](../../../../../data/javascript/svg/verification.json)

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

[Control adapter](../../../../../adapters/javascript/svg_browser.mjs)

## Run the valid control

[Browser container and control receipt](../../../../../projects/svg/javascript/stdlib_browser_image_decode/README.md)

```sh
python3 projects/svg/javascript/stdlib_browser_image_decode/verify-control.py
```

The browser runs this control, but its native parser source coverage and AFL++ parser feedback are unavailable. This path remains staged.
