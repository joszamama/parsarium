# HTMLImageElement.src = URL.createObjectURL(Blob({type:'image/svg+xml'})); decode(); canvas.drawImage() — SVG / JavaScript

- **Runtime:** Chromium 153.0.8010.12 via Playwright 1.63.0
- **Input API:** `HTMLImageElement.src = URL.createObjectURL(Blob({type:'image/svg+xml'})); decode(); canvas.drawImage()`
- **Official documentation:** [reference](https://html.spec.whatwg.org/multipage/embedded-content.html#the-img-element)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../../controls/svg/red-green.svg)
- **Inventory and verification:** [standard API record](../../../../../data/javascript/svg/standard.json) · [saved result](../../../../../data/javascript/svg/verification.json)

## Observed control result

2×1 decoded image with red and green RGBA pixels

[Control adapter](../../../../../adapters/javascript/svg_browser.mjs)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
