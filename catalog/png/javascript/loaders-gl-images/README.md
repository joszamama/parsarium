# @loaders.gl/images — PNG / JavaScript

- **Pinned release:** `4.5.4`
- **License:** MIT
- **Parsed scope:** header
- **Underlying family:** loaders.gl binary-image-api
- **Local input API:** `getBinaryImageMetadata(ArrayBuffer)`
- **Documentation:** [API reference](<https://loaders.gl/docs/modules/images/api-reference/binary-image-api>)
- **Catalog evidence:** [parser record](../../../../data/javascript/png/parsers.json) · [control verification](../../../../data/javascript/png/verification.json) · [within-ecosystem ranking](../../../../data/javascript/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "type": "png"
}
```

Reads encoded PNG header fields; does not decode pixels through this API.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
