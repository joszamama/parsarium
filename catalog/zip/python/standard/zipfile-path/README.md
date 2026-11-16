# zipfile.Path — ZIP / Python

- **Runtime:** CPython 3.13.1 standard library
- **Input API:** `zipfile.Path`
- **Official documentation:** [reference](https://docs.python.org/3.13/library/zipfile.html#zipfile.Path)
- **Valid control:** [`controls/zip/hello.zip`](../../../../../controls/zip/hello.zip)
- **Inventory and verification:** [standard API record](../../../../../data/python/zip/standard.json) · [saved result](../../../../../data/python/zip/verification.json)

**Parser family:** CPython zipfile

## Observed control result

```json
{
  "names": [
    "hello.txt"
  ],
  "hello": "parsarium\n"
}
```

[Control adapter](../../../../../adapters/python/zip/standard.py)

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
