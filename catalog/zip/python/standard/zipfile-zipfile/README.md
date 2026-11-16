# zipfile.ZipFile — ZIP / Python

- **Runtime:** CPython 3.13.1 standard library
- **Input API:** `zipfile.ZipFile`
- **Official documentation:** [reference](https://docs.python.org/3.13/library/zipfile.html#zipfile.ZipFile)
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

## Run this target

```sh
python3 parsarium.py build zip python stdlib_zipfile
python3 parsarium.py run zip python stdlib_zipfile controls/zip/hello.zip
```
