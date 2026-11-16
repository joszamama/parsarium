# archive/zip.OpenReader(path); File.Open() — ZIP / Go

- **Runtime:** Go 1.27.1 linux/arm64 standard library
- **Input API:** `archive/zip.OpenReader(path); File.Open()`
- **Official documentation:** [reference](https://pkg.go.dev/archive/zip@go1.27.1)
- **Valid control:** [`controls/zip/hello.zip`](../../../../../controls/zip/hello.zip)
- **Inventory and verification:** [standard API record](../../../../../data/go/zip/standard.json) · [saved result](../../../../../data/go/zip/verification.json)

## Observed control result

```json
{
  "name": "hello.txt",
  "text": "parsarium\n"
}
```

[Control adapter](../../../../../adapters/go/zip_std.go)

## Run this target

```sh
python3 parsarium.py build zip go stdlib_openreader
python3 parsarium.py run zip go stdlib_openreader controls/zip/hello.zip
```
