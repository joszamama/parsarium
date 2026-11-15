# oxvg_ast — SVG / Rust

- **Pinned release:** `0.0.9`
- **License:** MIT
- **Parsed scope:** SVG AST element structure
- **Underlying family:** oxvg_ast + roxmltree
- **Local input API:** `parse::roxmltree::parse(svg_text, callback) -> SVG AST`
- **Documentation:** [API reference](<https://docs.rs/oxvg_ast/0.0.9/oxvg_ast/parse/roxmltree/fn.parse.html>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "root": "svg",
  "elements": 2
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
