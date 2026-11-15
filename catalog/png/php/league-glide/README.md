# league/glide — PNG / PHP

- **Pinned release:** `4.1.0`
- **License:** MIT
- **Parsed scope:** decoded and re-encoded PNG dimensions
- **Underlying family:** Intervention Image / PHP GD PNG decoder
- **Local input API:** `ServerFactory::create with local source; Server::makeImage(PNG filename, parameters)`
- **Documentation:** [API reference](<https://github.com/thephpleague/glide/blob/54643c4c55ce6dc7f8a11d9c643340051d54c4d9/src/ServerFactory.php>)
- **Catalog evidence:** [parser record](../../../../data/php/png/parsers.json) · [control verification](../../../../data/php/png/verification.json) · [within-ecosystem ranking](../../../../data/php/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

Glide delegates to Intervention Image, configured to use PHP GD. This is a package path sharing both the Intervention Image package and GD decoder family.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
