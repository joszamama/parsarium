# parsson — JSON / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.1.9`
- **Upstream:** [source repository](<https://github.com/eclipse-ee4j/parsson>) · [Maven Central](<https://central.sonatype.com/artifact/org.eclipse.parsson/parsson>)
- **License:** EPL-2.0
- **Parser family:** Eclipse Parsson JsonParserImpl / JsonTokenizer
- **Local input API:** `new JsonProviderImpl().createParser(Files.newInputStream(local Path)); next(), getValue(), hasNext() to EOF`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/eclipse/parsson/parsson/1.1.9/parsson-1.1.9-sources.jar>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/java/json/parsers.json) · [control result](../../../../data/java/json/verification.json)

## Observed control result

```json
{
  "arrays": 3,
  "booleans": 2,
  "max_depth": 4,
  "nulls": 1,
  "numbers": [
    -2.5,
    1,
    1,
    2,
    2
  ],
  "objects": 5,
  "root": "object",
  "strings": [
    "café \"quoted\"",
    "go",
    "json",
    "parsarium",
    "rfc8259"
  ],
  "top_level_keys": [
    "enabled",
    "missing",
    "name",
    "nested",
    "ratio",
    "tags",
    "version"
  ]
}
```

## Run this target

```sh
python3 parsarium.py build json java parsson
python3 parsarium.py run json java parsson controls/json/nested-object.json
```
