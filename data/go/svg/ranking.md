# Go × SVG: verified parser ranking

21 verified third-party packages; working goal 20, original ceiling 30. The metric is pkg.go.dev's package-level ‘Imported by’ count captured at 2026-11-11T19:41:48.722283+00:00. It measures visible direct importers rather than downloads, and is used only within Go. 0 package(s) lack a metric and remain unranked; equal counts share a rank.

Search hits and unresolved leads are separate from this ranking. See `cell.json`, `registry-snapshot.json`, and `verification.json` in this directory.

| Rank | Package | Pinned module release | Imported by packages | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/tdewolff/minify/v2/svg](https://pkg.go.dev/github.com/tdewolff/minify/v2/svg@v2.24.25) | github.com/tdewolff/minify/v2@v2.24.25 | 159 | SVG-aware transformed colors and markup | tdewolff SVG minifier |
| 2 | [github.com/srwiley/oksvg](https://pkg.go.dev/github.com/srwiley/oksvg@v0.0.0-20221011165216-be6e8873101c) | github.com/srwiley/oksvg@v0.0.0-20221011165216-be6e8873101c | 130 | paths, width | oksvg lineage |
| 3 | [github.com/JoshVarga/svgparser](https://pkg.go.dev/github.com/JoshVarga/svgparser@v0.0.0-20200804023048-5eaba627a7d1) | github.com/JoshVarga/svgparser@v0.0.0-20200804023048-5eaba627a7d1 | 16 | rects, root | JoshVarga SVG tree parser |
| 4 | [github.com/rustyoz/svg](https://pkg.go.dev/github.com/rustyoz/svg@v0.0.0-20260625015314-1aeec84fa7e2) | github.com/rustyoz/svg@v0.0.0-20260625015314-1aeec84fa7e2 | 11 | height, width | rustyoz SVG parser |
| 5 | [github.com/boxesandglue/svgreader](https://pkg.go.dev/github.com/boxesandglue/svgreader@v0.0.9) | github.com/boxesandglue/svgreader@v0.0.9 | 6 | elements | boxesandglue SVG reader |
| 6 | [cogentcore.org/core/svg](https://pkg.go.dev/cogentcore.org/core/svg@v0.5.30) | cogentcore.org/core@v0.5.30 | 4 | parsed viewBox and two rectangle elements | Goki/Cogent SVG lineage |
| 7 | [github.com/lafriks/go-svg](https://pkg.go.dev/github.com/lafriks/go-svg@v0.5.1) | github.com/lafriks/go-svg@v0.5.1 | 3 | paths, width | oksvg lineage |
| 8 | [github.com/gen2brain/svg](https://pkg.go.dev/github.com/gen2brain/svg@v0.1.0) | github.com/gen2brain/svg@v0.1.0 | 2 | height, width | gen2brain SVG decoder |
| 8 | [github.com/pgavlin/svg2](https://pkg.go.dev/github.com/pgavlin/svg2) | github.com/pgavlin/svg2@v0.0.0-20210919231505-4ace7308edc1 | 2 | height, width | pgavlin SVG2 decoder |
| 10 | [github.com/benoitkugler/oksvg/svgicon](https://pkg.go.dev/github.com/benoitkugler/oksvg/svgicon@v0.0.0-20230818175515-13805796eb24) | github.com/benoitkugler/oksvg@v0.0.0-20230818175515-13805796eb24 | 1 | paths, width | oksvg lineage |
| 10 | [github.com/benoitkugler/webrender/svg](https://pkg.go.dev/github.com/benoitkugler/webrender/svg@v0.0.15) | github.com/benoitkugler/webrender@v0.0.15 | 1 | height, width | webrender SVG parser |
| 10 | [github.com/go-gfx/gfx/svg](https://pkg.go.dev/github.com/go-gfx/gfx/svg@v0.41.0) | github.com/go-gfx/gfx@v0.41.0 | 1 | height, width | go-gfx SVG rasterizer |
| 10 | [github.com/ironpark/ggfx/svg](https://pkg.go.dev/github.com/ironpark/ggfx/svg@v0.0.0-20261111143539-00f0f2c03daa) | github.com/ironpark/ggfx@v0.0.0-20261111143539-00f0f2c03daa | 1 | height, width | oksvg lineage |
| 10 | [github.com/sfomuseum/go-svg](https://pkg.go.dev/github.com/sfomuseum/go-svg@v0.0.0-20231208192434-a3c9facf873c) | github.com/sfomuseum/go-svg@v0.0.0-20231208192434-a3c9facf873c | 1 | height, width | sfomuseum SVG rasterizer |
| 10 | [goki.dev/svg](https://pkg.go.dev/goki.dev/svg@v0.1.28) | goki.dev/svg@v0.1.28 | 1 | parsed viewBox and two rectangle elements | Goki/Cogent SVG lineage |
| 16 | [github.com/NimbleMarkets/oksvg](https://pkg.go.dev/github.com/NimbleMarkets/oksvg@v0.1.6) | github.com/NimbleMarkets/oksvg@v0.1.6 | 0 | paths, width | oksvg lineage |
| 16 | [github.com/excitoon/coolsvg-go](https://pkg.go.dev/github.com/excitoon/coolsvg-go@v0.0.0-20260812001811-a8ecd1868275) | github.com/excitoon/coolsvg-go@v0.0.0-20260812001811-a8ecd1868275 | 0 | green, red, width | oksvg lineage |
| 16 | [github.com/fyne-io/oksvg](https://pkg.go.dev/github.com/fyne-io/oksvg@v0.2.0) | github.com/fyne-io/oksvg@v0.2.0 | 0 | paths, width | oksvg lineage |
| 16 | [github.com/golang-gui/oksvg](https://pkg.go.dev/github.com/golang-gui/oksvg@v0.1.0) | github.com/golang-gui/oksvg@v0.1.0 | 0 | paths, width | oksvg lineage |
| 16 | [github.com/shibukawa/bdf/image/svg](https://pkg.go.dev/github.com/shibukawa/bdf/image/svg@v0.2.1) | github.com/shibukawa/bdf@v0.2.1 | 0 | elements, root | shibukawa SVG tree parser |
| 16 | [github.com/vibrantgio/svg/parser](https://pkg.go.dev/github.com/vibrantgio/svg/parser@v0.1.3) | github.com/vibrantgio/svg@v0.1.3 | 0 | paths, width | oksvg lineage |
