# image.Decode(io.Reader) with image/png registered — PNG / Go

- **Runtime:** Go 1.27.1 linux/arm64 standard library
- **Input API:** `image.Decode(io.Reader) with image/png registered`
- **Official documentation:** [reference](https://pkg.go.dev/image@go1.27.1)
- **Valid control:** [`controls/png/red-green.png`](../../../../../controls/png/red-green.png)
- **Inventory and verification:** [standard API record](../../../../../data/go/png/standard.json) · [saved result](../../../../../data/go/png/verification.json)

## Observed control result

```json
{
  "format": "png",
  "height": 1,
  "width": 2
}
```

[Control adapter](../../../../../adapters/go/png_std.go)

## Run this target

```sh
python3 parsarium.py build png go stdlib_generic
python3 parsarium.py run png go stdlib_generic controls/png/red-green.png
```
