# jdk-jarinputstream — ZIP / Java

- **Runtime:** Eclipse Temurin OpenJDK 21.0.2
- **Input API:** `java.util.jar.JarInputStream(InputStream); getNextJarEntry/readAllBytes`
- **Official documentation:** [reference](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/jar/JarInputStream.html)
- **Valid control:** [`controls/zip/hello.zip`](../../../../../controls/zip/hello.zip)
- **Inventory and verification:** [standard API record](../../../../../data/java/zip/standard.json) · [saved result](../../../../../data/java/zip/verification.json)

**Parser family:** JDK ZipInputStream-derived JAR reader

## Observed control result

```json
{
  "name": "hello.txt",
  "content_base64": "cGFyc2FyaXVtCg=="
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
