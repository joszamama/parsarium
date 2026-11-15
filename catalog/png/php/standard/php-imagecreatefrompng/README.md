# php-imagecreatefrompng — PNG / PHP

- **Runtime:** PHP 8.5.12 CLI with GD 2.3.3
- **Input API:** `imagecreatefrompng(local PNG path); imagesx/imagesy; imagecolorat`
- **Official documentation:** [reference](https://www.php.net/manual/en/function.imagecreatefrompng.php)
- **Valid control:** [`controls/png/red-green.png`](../../../../../controls/png/red-green.png)
- **Inventory and verification:** [standard API record](../../../../../data/php/png/standard.json) · [saved result](../../../../../data/php/png/verification.json)

**Parser family:** PHP GD PNG decoder

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "left_rgb": [
    255,
    0,
    0
  ],
  "right_rgb": [
    0,
    255,
    0
  ]
}
```

[Control adapter](../../../../../adapters/php/png/runtime_imagecreatefrompng.php)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
