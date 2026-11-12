# JavaScript × Matrix Market: verified parser ranking

7 verified third-party packages; working goal 20, original ceiling 30. npm downloads cover 2026-10-11 through 2026-11-09 inclusive, counting all versions of each package name. This ranks adoption signals only within this cell.

Search hits and unresolved leads are separate from this ranking. See `cell.json`, `registry-snapshot.json`, and `verification.json` in this directory.

| Rank | Package | Pinned release | Downloads | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [@statelyai/graph](https://www.npmjs.com/package/@statelyai/graph/v/2.6.0) | 2.6.0 | 222,185 | Matrix Market graph vertices, edges, and edge weight | statelyai graph Matrix Market converter |
| 2 | [@msagl/parser](https://www.npmjs.com/package/@msagl/parser/v/1.1.24) | 1.1.24 | 140,762 | Graph edges from coordinate real general input; weights ignored | MSAGL parseTXT graph reader |
| 3 | [scran.js](https://www.npmjs.com/package/scran.js/v/4.1.0) | 4.1.0 | 399 | Symmetric coordinate matrix dimensions and value | scran.js/tatami Matrix Market WASM |
| 4 | [bakana](https://www.npmjs.com/package/bakana/v/3.1.3) | 3.1.3 | 116 | 10x Matrix Market matrix and companion feature/barcode files | scran.js/tatami Matrix Market WASM (wrapper) |
| 5 | [ngraph.serialization](https://www.npmjs.com/package/ngraph.serialization/v/0.0.8) | 0.0.8 | 60 | Matrix Market graph vertices, edges, and edge weight | ngraph.serialization MTX reader |
| 6 | [@jtgtools/xsparse](https://www.npmjs.com/package/@jtgtools/xsparse/v/0.0.1) | 0.0.1 | 20 | Coordinate real matrix dimensions and value | xsparse Matrix Market reader |
| 7 | [@orbifold/graphs](https://www.npmjs.com/package/@orbifold/graphs/v/4.0.3) | 4.0.3 | 8 | Graph edges from no-comment coordinate real general input | orbifold Matrix Market graph reader |

`scran.js` and `bakana` are separate npm package paths, but `bakana` calls the `scran.js` reader. The orbifold package's parser mishandled a valid comment-bearing control; its verified scope is the no-comment control only.

The `@msagl/parser` release publishes ESM with extensionless imports. The adapter uses pinned esbuild to bundle that release before calling its exported `parseTXT` API; this does not change the parser source.
