# jenssegers/imagehash — PNG / PHP

- **Pinned release:** `v0.11.0`
- **License:** MIT
- **Parsed scope:** decoded pixel-derived average hash
- **Underlying family:** Intervention Image 3 / PHP GD PNG decoder
- **Local input API:** `ImageHash(AverageHash, GD manager)::hash(local PNG path); toBits`
- **Documentation:** [API reference](<https://github.com/jenssegers/imagehash/blob/87ba7051d2fca2edc718091f052424474dedfeae/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "average_hash_bits": "0000111100001111000011110000111100001111000011110000111100001111"
}
```

ImageHash uses Intervention Image 3 with GD to decode PNG; separate Composer lock resolves the incompatible core major version.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
