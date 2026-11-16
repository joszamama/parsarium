# shutil.unpack_archive — ZIP / Python

- **Runtime:** CPython 3.13.1 standard library
- **Input API:** `shutil.unpack_archive`
- **Official documentation:** [reference](https://docs.python.org/3.13/library/shutil.html#shutil.unpack_archive)
- **Valid control:** [`controls/zip/hello.zip`](../../../../../controls/zip/hello.zip)
- **Inventory and verification:** [standard API record](../../../../../data/python/zip/standard.json) · [saved result](../../../../../data/python/zip/verification.json)

**Parser family:** CPython zipfile via shutil

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
python3 parsarium.py build zip python stdlib_unpack_archive
python3 parsarium.py run zip python stdlib_unpack_archive controls/zip/hello.zip
```
