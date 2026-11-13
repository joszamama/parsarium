# JavaScript × Matrix Market: verified parser ranking

8 verified third-party packages; working goal 20, original ceiling 30. npm downloads cover 2026-10-11 through 2026-11-09 inclusive, counting all versions of each package name. This ranks adoption signals only within this cell.

Search hits and unresolved leads are separate from this ranking. See `cell.json`, `registry-snapshot.json`, and `verification.json` in this directory.

| Rank | Package | Pinned release | Downloads | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [@statelyai/graph](https://www.npmjs.com/package/@statelyai/graph/v/2.6.0) | 2.6.0 | 222,185 | Matrix Market graph vertices, edges, and edge weight | statelyai graph Matrix Market converter |
| 2 | [@msagl/parser](https://www.npmjs.com/package/@msagl/parser/v/1.1.24) | 1.1.24 | 140,762 | Graph edges from coordinate real general input; weights ignored | MSAGL parseTXT graph reader |
| 3 | [keepset](https://github.com/Mearman/keepset/tree/v0.138.0) | 0.138.0 | 31,463 | Bipartite graph nodes and edges from coordinate real input; values ignored | keepset native Matrix Market graph parser |
| 4 | [scran.js](https://www.npmjs.com/package/scran.js/v/4.1.0) | 4.1.0 | 399 | Symmetric coordinate matrix dimensions and value | scran.js/tatami Matrix Market WASM |
| 5 | [bakana](https://www.npmjs.com/package/bakana/v/3.1.3) | 3.1.3 | 116 | 10x Matrix Market matrix and companion feature/barcode files | scran.js/tatami Matrix Market WASM (wrapper) |
| 6 | [ngraph.serialization](https://www.npmjs.com/package/ngraph.serialization/v/0.0.8) | 0.0.8 | 60 | Matrix Market graph vertices, edges, and edge weight | ngraph.serialization MTX reader |
| 7 | [@jtgtools/xsparse](https://www.npmjs.com/package/@jtgtools/xsparse/v/0.0.1) | 0.0.1 | 20 | Coordinate real matrix dimensions and value | xsparse Matrix Market reader |
| 8 | [@orbifold/graphs](https://www.npmjs.com/package/@orbifold/graphs/v/4.0.3) | 4.0.3 | 8 | Graph edges from no-comment coordinate real general input | orbifold Matrix Market graph reader |

`scran.js` and `bakana` are separate npm package paths, but `bakana` calls the `scran.js` reader. The orbifold package's parser mishandled a valid comment-bearing control; its verified scope is the no-comment control only.

The `@msagl/parser` release publishes ESM with extensionless imports. The adapter uses pinned esbuild to bundle that release before calling its exported `parseTXT` API; this does not change the parser source.

`keepset` 0.138.0's public `fetchEntry` accepts a documented injectable `FetchPort`. The adapter returns bytes read from the local valid control through this port and observes five bipartite nodes and three parsed edges. Its internal Matrix Market parser is in the pinned tagged source; no network service handles the control. Numeric matrix values are not exposed by this graph pathway. The 31,463 downloads place this package third under the same npm window, but do not measure Matrix Market use specifically. Twelve paths remain below the working goal.
