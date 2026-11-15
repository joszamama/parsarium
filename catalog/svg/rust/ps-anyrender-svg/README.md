# ps-anyrender-svg — SVG / Rust

- **Pinned release:** `0.15.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** SVG rendering scene commands
- **Underlying family:** ps-usvg fork via ps-anyrender-svg
- **Local input API:** `render_svg_str(&mut Scene, svg_text, Affine::IDENTITY)`
- **Documentation:** [API reference](<https://docs.rs/ps-anyrender-svg/0.15.0/ps_anyrender_svg/>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "render_commands": 2
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
