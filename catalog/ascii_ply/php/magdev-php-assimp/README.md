# magdev/php-assimp — ASCII PLY / PHP

- **Pinned release:** `0.3.2`
- **License:** MIT
- **Parsed scope:** One mesh with three vertices and one face reported from a valid local ASCII PLY triangle
- **Underlying family:** Assimp native PLY loader through magdev/php-assimp CLI wrapper
- **Local input API:** `Assimp\Command\Command::execute(new Assimp\Command\Verbs\InfoVerb(local filename), true); Result::getOutput`
- **Documentation:** [API reference](<https://github.com/magdev/php-assimp/blob/0.3.2/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/ascii_ply/parsers.json) · [control verification](../../../../data/php/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/php/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "meshes": 1,
  "vertices": 3,
  "faces": 1
}
```

The PHP 0.3.2 package invokes the external Assimp 6.0.6 CLI and returns its format-aware info output. It is a distinct PHP package path but shares Assimp PLY parsing with C/C++ paths. Version 0.6.0 is separately recorded as failing.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
