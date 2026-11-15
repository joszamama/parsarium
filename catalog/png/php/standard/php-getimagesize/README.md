# php-getimagesize — PNG / PHP

- **Runtime:** PHP 8.5.12 CLI with GD 2.3.3
- **Input API:** `getimagesize(local PNG path)`
- **Official documentation:** [reference](https://www.php.net/manual/en/function.getimagesize.php)
- **Valid control:** [`controls/png/red-green.png`](../../../../../controls/png/red-green.png)
- **Inventory and verification:** [standard API record](../../../../../data/php/png/standard.json) · [saved result](../../../../../data/php/png/verification.json)

**Parser family:** PHP image header reader

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "type": 3
}
```

[Control adapter](../../../../../adapters/php/png/runtime_getimagesize.php)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
