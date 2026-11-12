# Rust × SVG: verified parser ranking

25 verified third-party crate paths; working goal 20, original ceiling 30. The metric is crates.io crate-level recent downloads over 90 days, captured at 2026-11-12T01:56:22.795449+00:00. It includes all releases of each crate name and is compared only within Rust. 0 crate(s) lack a metric and remain unranked; equal counts share a rank.

Search hits, unresolved leads, and the standard-library inventory are separate from this ranking. See `cell.json`, `leads.json`, and `verification.json` in this directory.

| Rank | Crate | Pinned release | 90-day downloads | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [svgtypes](https://docs.rs/svgtypes/0.16.2/svgtypes/) | 0.16.2 | 16,856,466 | SVG path command grammar | svgtypes lineage |
| 2 | [usvg](https://docs.rs/usvg/0.50.0/usvg/) | 0.50.0 | 16,434,417 | SVG document tree and dimensions | usvg lineage |
| 3 | [resvg](https://docs.rs/resvg/0.50.0/resvg/) | 0.50.0 | 15,526,633 | SVG raster rendering | usvg lineage |
| 4 | [svg](https://docs.rs/svg/0.18.0/svg/) | 0.18.0 | 1,944,556 | SVG element event parsing | svg crate parser |
| 5 | [usvg-parser](https://docs.rs/usvg-parser/0.38.0/usvg_parser/) | 0.38.0 | 585,317 | SVG document tree and dimensions | usvg lineage |
| 6 | [svg-hush](https://docs.rs/svg-hush/0.9.7/svg_hush/) | 0.9.7 | 437,241 | SVG-aware stream filtering | svg-hush SVG filter |
| 7 | [anyrender_svg](https://docs.rs/anyrender_svg/0.15.0/anyrender_svg/) | 0.15.0 | 129,854 | SVG rendering scene commands | usvg lineage via anyrender_svg |
| 8 | [svg_path_ops](https://docs.rs/svg_path_ops/0.12.0/svg_path_ops/pt/struct.PathTransformer.html) | 0.12.0 | 77,230 | SVG path command grammar and serialization | svgtypes lineage via svg_path_ops |
| 9 | [spreet](https://docs.rs/spreet/0.14.0/spreet/) | 0.14.0 | 62,753 | SVG document tree and dimensions | usvg lineage via resvg |
| 10 | [vello_svg](https://docs.rs/vello_svg/0.11.0/vello_svg/) | 0.11.0 | 24,367 | SVG render path encoding | usvg lineage via vello_svg |
| 11 | [svgdom](https://docs.rs/svgdom/0.18.0/svgdom/) | 0.18.0 | 24,031 | SVG DOM elements | svgdom + svgtypes lineage |
| 12 | [oxvg_path](https://docs.rs/oxvg_path/0.0.9/oxvg_path/) | 0.0.9 | 21,580 | SVG path command grammar | oxvg_path + oxvg_parse |
| 13 | [svgrtypes](https://docs.rs/svgrtypes/0.50.2/svgrtypes/) | 0.50.2 | 21,500 | SVG path command grammar | svgtypes lineage fork |
| 14 | [usvgr](https://docs.rs/usvgr/0.50.2/usvgr/) | 0.50.2 | 21,426 | SVG document tree and dimensions | usvgr fork of usvg lineage |
| 15 | [oxvg_ast](https://docs.rs/oxvg_ast/0.0.9/oxvg_ast/parse/roxmltree/fn.parse.html) | 0.0.9 | 17,329 | SVG AST element structure | oxvg_ast + roxmltree |
| 16 | [svgr](https://docs.rs/svgr/0.50.2/svgr/) | 0.50.2 | 17,012 | SVG raster rendering | usvgr fork of usvg lineage |
| 17 | [librsvg](https://docs.rs/librsvg/2.63.4/rsvg/) | 2.63.4 | 16,035 | SVG document loading and intrinsic dimensions | librsvg SVG parser |
| 18 | [svg_metadata](https://docs.rs/svg_metadata/0.6.0/svg_metadata/) | 0.6.0 | 14,981 | SVG viewBox metadata | svg_metadata + roxmltree |
| 19 | [svgparser](https://docs.rs/svgparser/0.8.1/svgparser/) | 0.8.1 | 7,491 | SVG 1.1 element tokenization | svgparser |
| 20 | [ps-usvg](https://docs.rs/ps-usvg/0.48.1/usvg/) | 0.48.1 | 3,326 | SVG document tree and dimensions | ps-usvg fork of usvg lineage |
| 21 | [nsvg](https://docs.rs/nsvg/0.5.1/nsvg/) | 0.5.1 | 3,138 | SVG image dimensions via NanoSVG | NanoSVG C parser |
| 22 | [ps-anyrender-svg](https://docs.rs/ps-anyrender-svg/0.15.0/ps_anyrender_svg/) | 0.15.0 | 2,946 | SVG rendering scene commands | ps-usvg fork via ps-anyrender-svg |
| 23 | [ferrigura-path](https://docs.rs/ferrigura-path/0.7.0/ferrigura_path/) | 0.7.0 | 2,098 | SVG path geometry | Blink/Skia SVG path port |
| 24 | [svgcleaner](https://docs.rs/svgcleaner/0.9.5/svgcleaner/) | 0.9.5 | 1,461 | SVG DOM elements before cleaning | svgdom 0.10.5 |
| 25 | [oxideav-svg](https://docs.rs/oxideav-svg/0.2.0/oxideav_svg/fn.parse_from.html) | 0.2.0 | 904 | SVG document scene graph and dimensions | oxideav-svg native SVG parser |
