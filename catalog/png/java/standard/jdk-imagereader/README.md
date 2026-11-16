# jdk-imagereader — PNG / Java

- **Runtime:** Eclipse Temurin OpenJDK 21.0.2 linux/arm64 java.desktop
- **Input API:** `ImageIO.getImageReadersByFormatName("PNG"); ImageReader.setInput(ImageInputStream); read(0)`
- **Official documentation:** [reference](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/imageio/ImageReader.html)
- **Valid control:** [`controls/png/red-green.png`](../../../../../controls/png/red-green.png)
- **Inventory and verification:** [standard API record](../../../../../data/java/png/standard.json) · [saved result](../../../../../data/java/png/verification.json)

**Parser family:** JDK Image I/O PNG plugin

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "pixels": "ffff0000,ff00ff00"
}
```

## Run this target

```sh
python3 parsarium.py build png java jdk_imagereader
python3 parsarium.py run png java jdk_imagereader controls/png/red-green.png
```
