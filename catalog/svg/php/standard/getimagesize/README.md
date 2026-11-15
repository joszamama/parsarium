# getimagesize — SVG / PHP

- **Runtime:** PHP 8.5.12 CLI with ext-libxml
- **Input API:** `getimagesize(local SVG file path); PHP 8.5 added SVG dimension parsing with ext-libxml`
- **Official documentation:** [reference](https://www.php.net/manual/en/function.getimagesize.php) · [reference](https://www.php.net/manual/en/migration85.new-features.php)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../../controls/svg/red-green.svg)
- **Inventory and verification:** [standard API record](../../../../../data/php/svg/standard.json) · [saved result](../../../../../data/php/svg/verification.json)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "mime": "image/svg+xml",
  "width_unit": "px",
  "height_unit": "px"
}
```

[Control adapter](../../../../../adapters/php/svg/runtime_probe.php)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
