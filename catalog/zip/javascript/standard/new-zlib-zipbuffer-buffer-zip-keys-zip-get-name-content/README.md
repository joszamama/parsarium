# new zlib.ZipBuffer(Buffer); zip.keys(); zip.get(name).content() — ZIP / JavaScript

- **Runtime:** Node.js 26.10.0
- **Input API:** `new zlib.ZipBuffer(Buffer); zip.keys(); zip.get(name).content()`
- **Official documentation:** [reference](https://nodejs.org/docs/v26.10.0/api/zlib.html#class-zlibzipbuffer)
- **Valid control:** [`controls/zip/hello.zip`](../../../../../controls/zip/hello.zip)
- **Inventory and verification:** [standard API record](../../../../../data/javascript/zip/standard.json) · [saved result](../../../../../data/javascript/zip/verification.json)

## Observed control result

```json
{
  "entries": [
    "hello.txt"
  ],
  "content": "parsarium\n"
}
```

[Control adapter](../../../../../adapters/javascript/zip_node.mjs)

## Run this target

```sh
python3 parsarium.py build zip javascript stdlib_node_zipbuffer
python3 parsarium.py run zip javascript stdlib_node_zipbuffer controls/zip/hello.zip
```
