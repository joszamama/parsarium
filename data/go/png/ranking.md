# Go × PNG: verified parser ranking

20 verified third-party packages; working goal 20, original ceiling 30. The metric is pkg.go.dev's package-level ‘Imported by’ count captured at 2026-11-11T18:34:56.475538+00:00. It measures visible direct importers rather than downloads, and is used only within Go. 0 package(s) lack a metric and remain unranked; equal counts share a rank.

Search hits and unresolved leads are separate from this ranking. See `cell.json`, `registry-snapshot.json`, and `verification.json` in this directory.

| Rank | Package | Pinned module release | Imported by packages | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/disintegration/imaging](https://pkg.go.dev/github.com/disintegration/imaging@v1.6.2) | github.com/disintegration/imaging@v1.6.2 | 3,155 | pixels | Go image/png wrapper |
| 2 | [github.com/fogleman/gg](https://pkg.go.dev/github.com/fogleman/gg@v1.3.0) | github.com/fogleman/gg@v1.3.0 | 1,942 | pixels | Go image/png wrapper |
| 3 | [gopkg.in/gographics/imagick.v3/imagick](https://pkg.go.dev/gopkg.in/gographics/imagick.v3/imagick@v3.7.3) | gopkg.in/gographics/imagick.v3@v3.7.3 | 309 | dimensions | ImageMagick MagickWand |
| 4 | [github.com/h2non/bimg](https://pkg.go.dev/github.com/h2non/bimg@v1.1.9) | github.com/h2non/bimg@v1.1.9 | 180 | dimensions | libvips |
| 5 | [github.com/davidbyttow/govips/v2/vips](https://pkg.go.dev/github.com/davidbyttow/govips/v2/vips@v2.20.0) | github.com/davidbyttow/govips/v2@v2.20.0 | 135 | dimensions | libvips |
| 6 | [github.com/anthonynsimon/bild/imgio](https://pkg.go.dev/github.com/anthonynsimon/bild/imgio@v0.17.1) | github.com/anthonynsimon/bild@v0.17.1 | 125 | pixels | Go image/png wrapper |
| 7 | [github.com/andrianbdn/iospng](https://pkg.go.dev/github.com/andrianbdn/iospng@v0.0.0-20180730113000-dccef1992541) | github.com/andrianbdn/iospng@v0.0.0-20180730113000-dccef1992541 | 27 | dimensions+converted_bytes | iOS PNG converter |
| 8 | [github.com/dsoprea/go-png-image-structure/v2](https://pkg.go.dev/github.com/dsoprea/go-png-image-structure/v2@v2.0.0-20210512210324-29b889a6093d) | github.com/dsoprea/go-png-image-structure/v2@v2.0.0-20210512210324-29b889a6093d | 24 | chunks+dimensions | PNG chunk structure parser |
| 9 | [github.com/gameparrot/fastpng](https://pkg.go.dev/github.com/gameparrot/fastpng@v0.0.0-20250305185850-d72e123a2123) | github.com/gameparrot/fastpng@v0.0.0-20250305185850-d72e123a2123 | 8 | pixels | Go image/png-derived decoder |
| 10 | [github.com/go-images/png](https://pkg.go.dev/github.com/go-images/png@v0.2.0) | github.com/go-images/png@v0.2.0 | 1 | pixels | Go image/png fork |
| 10 | [github.com/m8rge/go-scaled-png](https://pkg.go.dev/github.com/m8rge/go-scaled-png@v1.0.0) | github.com/m8rge/go-scaled-png@v1.0.0 | 1 | pixels | Go image/png fork with scaling |
| 12 | [github.com/fumin/png](https://pkg.go.dev/github.com/fumin/png@v0.0.0-20220417120418-2266efc3c1a5) | github.com/fumin/png@v0.0.0-20220417120418-2266efc3c1a5 | 0 | pixels | Go image/png fork |
| 12 | [github.com/gen2brain/pngn](https://pkg.go.dev/github.com/gen2brain/pngn@v0.1.3) | github.com/gen2brain/pngn@v0.1.3 | 0 | pixels | pngn decoder |
| 12 | [github.com/knoweather/simple-png](https://pkg.go.dev/github.com/knoweather/simple-png@v1.5.0) | github.com/knoweather/simple-png@v1.5.0 | 0 | pixels | simple-png decoder |
| 12 | [github.com/magical/png](https://pkg.go.dev/github.com/magical/png@v0.0.0-20131112000825-bf2aaca8f4d6) | github.com/magical/png@v0.0.0-20131112000825-bf2aaca8f4d6 | 0 | pixels | Go image/png fork |
| 12 | [github.com/mduvall/go-image-png/png](https://pkg.go.dev/github.com/mduvall/go-image-png/png@v0.0.0-20150701034220-46bfaa3c2537) | github.com/mduvall/go-image-png@v0.0.0-20150701034220-46bfaa3c2537 | 0 | pixels | Go image/png fork |
| 12 | [github.com/oyamo/pngx](https://pkg.go.dev/github.com/oyamo/pngx@v0.0.0-20230307064515-ec4b3bce8a92) | github.com/oyamo/pngx@v0.0.0-20230307064515-ec4b3bce8a92 | 0 | pixels | Go image/png fork |
| 12 | [github.com/shogo82148/go-imaging/png](https://pkg.go.dev/github.com/shogo82148/go-imaging/png@v0.2.0) | github.com/shogo82148/go-imaging@v0.2.0 | 0 | pixels | Go image/png fork |
| 12 | [github.com/tdewolff/canvas/image](https://pkg.go.dev/github.com/tdewolff/canvas/image@v0.0.0-20260923214215-09804640d00c) | github.com/tdewolff/canvas@v0.0.0-20260923214215-09804640d00c | 0 | pixels | canvas PNG image loader |
| 12 | [github.com/woozymasta/png](https://pkg.go.dev/github.com/woozymasta/png@v1.2.0) | github.com/woozymasta/png@v1.2.0 | 0 | pixels | Go image/png fork |
