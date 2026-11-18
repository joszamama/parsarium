# GO × ASCII PLY: selected parsers

9 control-verified third-party paths selected from 24 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

pkg.go.dev Imported by package count.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/fogleman/fauxgl](https://pkg.go.dev/github.com/fogleman/fauxgl@v0.0.0-20250110135958-abf826acbbbd#LoadPLY) | v0.0.0-20250110135958-abf826acbbbd | 303 | ASCII PLY header, vertex x/y/z rows and vertex_indices face rows converted to a triangle mesh | fauxgl native Go PLY reader (ply.go) |
| 2 | [go.viam.com/rdk/spatialmath](https://pkg.go.dev/go.viam.com/rdk@v1.17.0/spatialmath#NewMeshFromPLYFile) | v1.17.0 | 44 | ASCII PLY triangle faces converted to millimetre-scaled triangles | Viam RDK spatialmath mesh loader over goply (shared goply parser family) |
| 3 | [github.com/unixpickle/model3d/model3d](https://pkg.go.dev/github.com/unixpickle/model3d@v0.4.23/model3d#ReadColorPLY) | v0.4.23 | 23 | ASCII PLY with x/y/z (optional red/green/blue) vertices and a vertex_index triangle face list, returned as triangles and a vertex colour map | model3d mesh reader over the model3d fileformats PLYReader (shared model3d PLY parser family) |
| 4 | [github.com/tbogdala/assimp-go](https://pkg.go.dev/github.com/tbogdala/assimp-go@v0.0.0-20160907223021-d10e2135f9fe) | v0.0.0-20160907223021-d10e2135f9fe | 4 | ASCII PLY mesh, vertex, and face counts | Assimp C++ importer |
| 5 | [github.com/EliCDavis/polyform/formats/ply](https://pkg.go.dev/github.com/EliCDavis/polyform@v0.44.0/formats/ply) | v0.44.0 | 2 | ASCII PLY vertex and face counts | polyform PLY |
| 6 | [github.com/bloeys/assimp-go/asig](https://pkg.go.dev/github.com/bloeys/assimp-go@v0.6.0/asig) | v0.6.0 | 1 | ASCII PLY mesh, vertex, and face counts | Assimp C++ importer |
| 7 | [github.com/chenzhekl/goply](https://pkg.go.dev/github.com/chenzhekl/goply@v0.0.0-20190930133256-258c2381defd) | v0.0.0-20190930133256-258c2381defd | 1 | ASCII PLY vertex and face counts | goply |
| 8 | [github.com/rishabh-bector/assimp-golang](https://pkg.go.dev/github.com/rishabh-bector/assimp-golang@v0.0.0-20190130041627-cbac4dcfdaf3) | v0.0.0-20190130041627-cbac4dcfdaf3 | 1 | ASCII PLY mesh, vertex, and face counts | Assimp C++ importer |
| 9 | [github.com/thebanri/limoni/graphics](https://pkg.go.dev/github.com/thebanri/limoni@v0.16.0/graphics) | v0.16.0 | 1 | ASCII PLY vertex and face counts | limoni PLY |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
