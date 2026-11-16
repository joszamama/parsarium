# jdk-toolkit — PNG / Java

- **Runtime:** Eclipse Temurin OpenJDK 21.0.2 linux/arm64 java.desktop
- **Input API:** `Toolkit.getDefaultToolkit().createImage(byte[])`
- **Official documentation:** [reference](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/java/awt/Toolkit.html)
- **Valid control:** [`controls/png/red-green.png`](../../../../../controls/png/red-green.png)
- **Inventory and verification:** [standard API record](../../../../../data/java/png/standard.json) · [saved result](../../../../../data/java/png/verification.json)

**Parser family:** AWT Toolkit PNG reader

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "pixels": "ffff0000,ff00ff00"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
