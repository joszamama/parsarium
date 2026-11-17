# GO × ASCII PLY: selected parsers

7 control-verified third-party paths selected from 22 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

pkg.go.dev Imported by package count.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [go.viam.com/rdk/spatialmath](https://pkg.go.dev/go.viam.com/rdk@v1.17.0/spatialmath#NewMeshFromPLYFile) | v1.17.0 | 44 | ASCII PLY triangle faces converted to millimetre-scaled triangles | Viam RDK spatialmath mesh loader over goply (shared goply parser family) |
| 2 | [github.com/tbogdala/assimp-go](https://pkg.go.dev/github.com/tbogdala/assimp-go@v0.0.0-20160907223021-d10e2135f9fe) | v0.0.0-20160907223021-d10e2135f9fe | 4 | ASCII PLY mesh, vertex, and face counts | Assimp C++ importer |
| 3 | [github.com/EliCDavis/polyform/formats/ply](https://pkg.go.dev/github.com/EliCDavis/polyform@v0.44.0/formats/ply) | v0.44.0 | 2 | ASCII PLY vertex and face counts | polyform PLY |
| 4 | [github.com/bloeys/assimp-go/asig](https://pkg.go.dev/github.com/bloeys/assimp-go@v0.6.0/asig) | v0.6.0 | 1 | ASCII PLY mesh, vertex, and face counts | Assimp C++ importer |
| 5 | [github.com/chenzhekl/goply](https://pkg.go.dev/github.com/chenzhekl/goply@v0.0.0-20190930133256-258c2381defd) | v0.0.0-20190930133256-258c2381defd | 1 | ASCII PLY vertex and face counts | goply |
| 6 | [github.com/rishabh-bector/assimp-golang](https://pkg.go.dev/github.com/rishabh-bector/assimp-golang@v0.0.0-20190130041627-cbac4dcfdaf3) | v0.0.0-20190130041627-cbac4dcfdaf3 | 1 | ASCII PLY mesh, vertex, and face counts | Assimp C++ importer |
| 7 | [github.com/thebanri/limoni/graphics](https://pkg.go.dev/github.com/thebanri/limoni@v0.16.0/graphics) | v0.16.0 | 1 | ASCII PLY vertex and face counts | limoni PLY |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
