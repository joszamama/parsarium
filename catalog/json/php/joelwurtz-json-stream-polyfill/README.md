# joelwurtz/json-stream-polyfill — JSON / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.1.0`
- **License:** MIT
- **Parser family:** json_stream polyfill structural scanner (pure-PHP port of the json_stream extension) plus PHP ext/json for scalar tokens
- **Local input API:** `json_stream_decode(string $source) with default options over local bytes; returns a lazy JsonStream\Document whose foreach iteration yields member names/indexes, scalars and child Documents for nested containers; the container kind is read from the documented __debugInfo() 'kind'. The harness type-tags the yielded tree with members in returned order and never calls toValue(). The image deletes only the package's bootstrap.php entry from the Composer-generated autoload_files.php and autoload_static.php (asserted in the Dockerfile), and harness.php loads bootstrap.php with the README-documented manual require after vendor/autoload.php, so php-fuzzer instruments the polyfill source; package files are unchanged and diffed against the pinned archive.`
- **Documentation:** [API reference](<https://github.com/joelwurtz/php-json-stream-polyfill/blob/0136c414d2100f779dffd8910e5d591f97845004/README.md#what-it-implements>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/php/json/parsers.json) · [control result](../../../../data/php/json/verification.json)

## Observed control result

```json
{
  "type": "object",
  "members": {
    "name": {
      "type": "string",
      "value": "parsarium"
    },
    "version": {
      "type": "number",
      "value": 1
    },
    "ratio": {
      "type": "number",
      "value": -2.5
    },
    "enabled": {
      "type": "boolean",
      "value": true
    },
    "missing": {
      "type": "null"
    },
    "tags": {
      "type": "array",
      "items": [
        {
          "type": "string",
          "value": "json"
        },
        {
          "type": "string",
          "value": "go"
        },
        {
          "type": "string",
          "value": "rfc8259"
        }
      ]
    },
    "nested": {
      "type": "object",
      "members": {
        "level": {
          "type": "number",
          "value": 2
        },
        "items": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "members": {
                "id": {
                  "type": "number",
                  "value": 1
                },
                "ok": {
                  "type": "boolean",
                  "value": false
                }
              }
            },
            {
              "type": "object",
              "members": {
                "id": {
                  "type": "number",
                  "value": 2
                },
                "text": {
                  "type": "string",
                  "value": "café \"quoted\""
                }
              }
            }
          ]
        },
        "empty": {
          "type": "object",
          "members": {}
        },
        "list": {
          "type": "array",
          "items": []
        }
      }
    }
  }
}
```

## Run this target

```sh
python3 parsarium.py build json php joelwurtz_json_stream_polyfill
python3 parsarium.py run json php joelwurtz_json_stream_polyfill controls/json/nested-object.json
```
