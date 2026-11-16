# zipimport.zipimporter — ZIP / Python

- **Runtime:** CPython 3.13.1 standard library
- **Input API:** `zipimport.zipimporter`
- **Official documentation:** [reference](https://docs.python.org/3.13/library/zipimport.html#zipimport.zipimporter)
- **Valid control:** [`controls/zip/hello-module.zip`](../../../../../controls/zip/hello-module.zip)
- **Inventory and verification:** [standard API record](../../../../../data/python/zip/standard.json) · [saved result](../../../../../data/python/zip/verification.json)

**Parser family:** CPython zipimport ZIP reader

## Observed control result

```json
{
  "source": "message = 'parsarium'\n"
}
```

[Control adapter](../../../../../adapters/python/zip/standard.py)

## Run this target

```sh
python3 parsarium.py build zip python stdlib_zipimport
python3 parsarium.py run zip python stdlib_zipimport controls/zip/hello-module.zip
```
