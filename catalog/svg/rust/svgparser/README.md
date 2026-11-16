# svgparser — SVG / Rust

- **Pinned release:** `0.8.1`
- **License:** MIT/Apache-2.0
- **Parsed scope:** SVG 1.1 element tokenization
- **Underlying family:** svgparser
- **Local input API:** `svg::Tokenizer::from_str(svg_text) -> Token::ElementStart`
- **Documentation:** [API reference](<https://docs.rs/svgparser/0.8.1/svgparser/>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "rects": 2
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/rust/svgparser/README.md)

```sh
python3 parsarium.py build svg rust svgparser
python3 parsarium.py run svg rust svgparser controls/svg/red-green.svg
```
