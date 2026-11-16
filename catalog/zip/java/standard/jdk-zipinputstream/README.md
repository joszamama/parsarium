# jdk-zipinputstream — ZIP / Java

- **Runtime:** Eclipse Temurin OpenJDK 21.0.2 linux/arm64 java.base
- **Input API:** `java.util.zip.ZipInputStream(InputStream); getNextEntry/readAllBytes`
- **Official documentation:** [reference](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/zip/ZipInputStream.html)
- **Valid control:** [`controls/zip/hello.zip`](../../../../../controls/zip/hello.zip)
- **Inventory and verification:** [standard API record](../../../../../data/java/zip/standard.json) · [saved result](../../../../../data/java/zip/verification.json)

**Parser family:** JDK ZIP stream reader

## Observed control result

```json
{
  "name": "hello.txt",
  "content_base64": "cGFyc2FyaXVtCg=="
}
```

## Run this target

```sh
python3 parsarium.py build zip java jdk_zipinputstream
python3 parsarium.py run zip java jdk_zipinputstream controls/zip/hello.zip
```
