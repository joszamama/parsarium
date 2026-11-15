# sfml — PNG / C++

- **Pinned release:** `3.0.2`
- **License:** Zlib
- **Parsed scope:** RGBA pixels
- **Underlying family:** SFML bundled stb_image PNG decoder
- **Local input API:** `sf::Image::loadFromFile(const std::filesystem::path&); getSize(); getPixel(sf::Vector2u)`
- **Documentation:** [API reference](<https://www.sfml-dev.org/documentation/3.0.2/classsf_1_1Image.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/png/parsers.json) · [control verification](../../../../data/cpp/png/verification.json) · [within-ecosystem ranking](../../../../data/cpp/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first": [
    255,
    0,
    0,
    255
  ],
  "second": [
    0,
    255,
    0,
    255
  ]
}
```

The pinned Image.cpp embeds stb_image and calls stbi_load_from_callbacks; this shares decoder lineage with the verified stb and raylib paths.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
