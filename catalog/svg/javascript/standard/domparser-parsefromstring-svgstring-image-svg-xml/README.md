# DOMParser.parseFromString(svgString, 'image/svg+xml') — SVG / JavaScript

- **Runtime:** Chromium 153.0.8010.12 via Playwright 1.63.0
- **Input API:** `DOMParser.parseFromString(svgString, 'image/svg+xml')`
- **Official documentation:** [reference](https://w3c.github.io/DOM-Parsing/#dom-domparser-parsefromstring)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../../controls/svg/red-green.svg)
- **Inventory and verification:** [standard API record](../../../../../data/javascript/svg/standard.json) · [saved result](../../../../../data/javascript/svg/verification.json)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rects": 2,
  "fills": [
    "#ff0000",
    "#00ff00"
  ],
  "typed_root": true,
  "typed_rects": true
}
```

[Control adapter](../../../../../adapters/javascript/svg_browser.mjs)

## Run the valid control

[Browser container and control receipt](../../../../../projects/svg/javascript/stdlib_browser_domparser/README.md)

```sh
python3 projects/svg/javascript/stdlib_browser_domparser/verify-control.py
```

The browser runs this control, but its native parser source coverage and AFL++ parser feedback are unavailable. This path remains staged.
