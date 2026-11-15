# archive/zip.OpenReader(path); File.Open() — ZIP / Go

- **Runtime:** Go 1.27.1 darwin/arm64 standard library
- **Input API:** `archive/zip.OpenReader(path); File.Open()`
- **Official documentation:** [reference](https://pkg.go.dev/archive/zip@go1.27.1)
- **Valid control:** [`controls/zip/hello.zip`](../../../../../controls/zip/hello.zip)
- **Inventory and verification:** [standard API record](../../../../../data/go/zip/standard.json) · [saved result](../../../../../data/go/zip/verification.json)

## Observed control result

One entry named hello.txt containing parsarium followed by a newline

[Control adapter](../../../../../adapters/go/zip_std.go)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
