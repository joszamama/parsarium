# Go × ASCII PNM: verified parser ranking

20 verified third-party packages; working goal 20, original ceiling 30. The metric is pkg.go.dev's package-level ‘Imported by’ count captured at 2026-11-11T19:57:08.163004+00:00. It measures visible direct importers rather than downloads, and is used only within Go. 0 package(s) lack a metric and remain unranked; equal counts share a rank.

Search hits and unresolved leads are separate from this ranking. See `cell.json`, `registry-snapshot.json`, and `verification.json` in this directory.

| Rank | Package | Pinned module release | Imported by packages | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [gopkg.in/gographics/imagick.v3/imagick](https://pkg.go.dev/gopkg.in/gographics/imagick.v3/imagick@v3.7.3) | gopkg.in/gographics/imagick.v3@v3.7.3 | 309 | P3 dimensions | ImageMagick |
| 2 | [github.com/jbuchbinder/gopnm](https://pkg.go.dev/github.com/jbuchbinder/gopnm@v0.0.0-20251119211316-bb594e0d2e34) | github.com/jbuchbinder/gopnm@v0.0.0-20251119211316-bb594e0d2e34 | 42 | P3 pixels and dimensions | gopnm lineage |
| 3 | [github.com/spakin/netpbm](https://pkg.go.dev/github.com/spakin/netpbm@v1.3.2) | github.com/spakin/netpbm@v1.3.2 | 17 | P3 pixels and dimensions | spakin Netpbm |
| 4 | [github.com/go-gfx/gfx/codec](https://pkg.go.dev/github.com/go-gfx/gfx/codec@v0.41.0) | github.com/go-gfx/gfx@v0.41.0 | 8 | P3 pixels and dimensions | go-gfx PNM decoder |
| 5 | [github.com/UNO-SOFT/gopnm](https://pkg.go.dev/github.com/UNO-SOFT/gopnm@v0.0.2) | github.com/UNO-SOFT/gopnm@v0.0.2 | 2 | P3 pixels and dimensions | gopnm lineage |
| 5 | [github.com/harrydb/go/img/pnm](https://pkg.go.dev/github.com/harrydb/go/img/pnm@v0.0.0-20160105214235-0ff7a05d1aa4) | github.com/harrydb/go@v0.0.0-20160105214235-0ff7a05d1aa4 | 2 | P3 pixels and dimensions | peterh/go PNM lineage |
| 7 | [github.com/hexaflex/pnm](https://pkg.go.dev/github.com/hexaflex/pnm@v0.0.0-20200810192450-e891a41ac33b) | github.com/hexaflex/pnm@v0.0.0-20200810192450-e891a41ac33b | 1 | P3 pixels and dimensions | hexaflex PNM |
| 8 | [codeberg.org/rabenauge/picsetgo/formats/netpbm](https://pkg.go.dev/codeberg.org/rabenauge/picsetgo/formats/netpbm@v0.5.6) | codeberg.org/rabenauge/picsetgo@v0.5.6 | 0 | P3 pixels and dimensions | picsetgo Netpbm |
| 8 | [gitee.com/shiqiyue/go-vips](https://pkg.go.dev/gitee.com/shiqiyue/go-vips@v0.0.1) | gitee.com/shiqiyue/go-vips@v0.0.1 | 0 | P3 dimensions | libvips ppmload |
| 8 | [github.com/571451370/go-media/image/pnm](https://pkg.go.dev/github.com/571451370/go-media/image/pnm@v0.0.0-20190312080447-697b98554cbd) | github.com/571451370/go-media@v0.0.0-20190312080447-697b98554cbd | 0 | P3 pixels and dimensions | go-media PNM |
| 8 | [github.com/bu/govips/pkg/vips](https://pkg.go.dev/github.com/bu/govips/pkg/vips@v0.0.0-20191224162542-9c70e55b5850) | github.com/bu/govips@v0.0.0-20191224162542-9c70e55b5850 | 0 | P3 pixels and dimensions | libvips ppmload |
| 8 | [github.com/jcbritobr/pnm](https://pkg.go.dev/github.com/jcbritobr/pnm@v0.1.0) | github.com/jcbritobr/pnm@v0.1.0 | 0 | P3 header: dimensions and maximum channel value | jcbritobr PNM |
| 8 | [github.com/kirklin/vipsx/vips](https://pkg.go.dev/github.com/kirklin/vipsx/vips@v0.5.1) | github.com/kirklin/vipsx@v0.5.1 | 0 | P3 dimensions | libvips ppmload |
| 8 | [github.com/kovidgoyal/imaging/netpbm](https://pkg.go.dev/github.com/kovidgoyal/imaging/netpbm@v1.9.0) | github.com/kovidgoyal/imaging@v1.9.0 | 0 | P3 pixels and dimensions | kovidgoyal Netpbm |
| 8 | [github.com/ncruces/go-pnm](https://pkg.go.dev/github.com/ncruces/go-pnm@v1.0.0) | github.com/ncruces/go-pnm@v1.0.0 | 0 | P3 pixels and dimensions | gopnm lineage |
| 8 | [github.com/perelin/govips/pkg/vips](https://pkg.go.dev/github.com/perelin/govips/pkg/vips@v0.0.0-20200811153805-fbe430bb7feb) | github.com/perelin/govips@v0.0.0-20200811153805-fbe430bb7feb | 0 | P3 pixels and dimensions | libvips ppmload |
| 8 | [github.com/peterh/go/img/pnm](https://pkg.go.dev/github.com/peterh/go/img/pnm@v0.0.0-20140610174529-c4962588ab84) | github.com/peterh/go@v0.0.0-20140610174529-c4962588ab84 | 0 | P3 pixels and dimensions | peterh/go PNM lineage |
| 8 | [github.com/robxyy/govips/pkg/vips](https://pkg.go.dev/github.com/robxyy/govips/pkg/vips@v0.0.0-20180604122901-95ac1cf58567) | github.com/robxyy/govips@v0.0.0-20180604122901-95ac1cf58567 | 0 | P3 pixels and dimensions | libvips ppmload |
| 8 | [github.com/shogo82148/go-imaging/pnm](https://pkg.go.dev/github.com/shogo82148/go-imaging/pnm@v0.2.0) | github.com/shogo82148/go-imaging@v0.2.0 | 0 | P3 pixels and dimensions | shogo82148 PNM |
| 8 | [github.com/wkqco33/tdraw/pnm](https://pkg.go.dev/github.com/wkqco33/tdraw/pnm@v0.7.0) | github.com/wkqco33/tdraw@v0.7.0 | 0 | P3 pixels and dimensions | tdraw PNM |
