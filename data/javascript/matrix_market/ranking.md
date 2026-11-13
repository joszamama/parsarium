# JavaScript × Matrix Market: verified parser ranking

9 verified third-party package paths; working goal 20, original ceiling 30. npm downloads cover 2026-10-11 through 2026-11-09 inclusive, counting all versions of each package name. This ranks adoption signals only within this cell.

Search hits and unresolved leads are separate from this ranking. See `cell.json`, `registry-snapshot.json`, and `verification.json` in this directory.

| Rank | Package | Pinned release | Downloads | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [@statelyai/graph](https://www.npmjs.com/package/@statelyai/graph/v/2.6.0) | 2.6.0 | 222,185 | Matrix Market graph vertices, edges, and edge weight | statelyai graph Matrix Market converter |
| 2 | [@msagl/parser](https://www.npmjs.com/package/@msagl/parser/v/1.1.24) | 1.1.24 | 140,762 | Graph edges from coordinate real general input; weights ignored | MSAGL parseTXT graph reader |
| 3 | [keepset](https://github.com/Mearman/keepset/tree/v0.138.0) | 0.138.0 | 31,463 | Bipartite graph nodes and edges from coordinate real input; values ignored | keepset native Matrix Market graph parser |
| 4 | [graphbox](https://github.com/Mearman/GraphBox/blob/v1.4.6/src/formats/mtx/index.ts) | 1.4.6 tagged source | 896 | Coordinate real matrix dimensions, entries, value type, symmetry, and value | GraphBox native Matrix Market document parser |
| 5 | [scran.js](https://www.npmjs.com/package/scran.js/v/4.1.0) | 4.1.0 | 399 | Symmetric coordinate matrix dimensions and value | scran.js/tatami Matrix Market WASM |
| 6 | [bakana](https://www.npmjs.com/package/bakana/v/3.1.3) | 3.1.3 | 116 | 10x Matrix Market matrix and companion feature/barcode files | scran.js/tatami Matrix Market WASM (wrapper) |
| 7 | [ngraph.serialization](https://www.npmjs.com/package/ngraph.serialization/v/0.0.8) | 0.0.8 | 60 | Matrix Market graph vertices, edges, and edge weight | ngraph.serialization MTX reader |
| 8 | [@jtgtools/xsparse](https://www.npmjs.com/package/@jtgtools/xsparse/v/0.0.1) | 0.0.1 | 20 | Coordinate real matrix dimensions and value | xsparse Matrix Market reader |
| 9 | [@orbifold/graphs](https://www.npmjs.com/package/@orbifold/graphs/v/4.0.3) | 4.0.3 | 8 | Graph edges from no-comment coordinate real general input | orbifold Matrix Market graph reader |

`scran.js` and `bakana` are separate npm package paths, but `bakana` calls the `scran.js` reader. The orbifold package's parser mishandled a valid comment-bearing control; its verified scope is the no-comment control only.

The `@msagl/parser` release publishes ESM with extensionless imports. The adapter uses pinned esbuild to bundle that release before calling its exported `parseTXT` API; this does not change the parser source.

`keepset` 0.138.0's public `fetchEntry` accepts a documented injectable `FetchPort`. The adapter returns bytes read from the local valid control through this port and observes five bipartite nodes and three parsed edges. Its internal Matrix Market parser is in the pinned tagged source; no network service handles the control. Numeric matrix values are not exposed by this graph pathway. The 31,463 downloads place this package third under the same npm window, but do not measure Matrix Market use specifically.

`graphbox` 1.4.6 exports `parseMtx(local text)` from its tagged source. The adapter compiles only that public parser with pinned esbuild and observes the valid 2×3 matrix, three entries, real/general header fields and value −2. The published npm 1.4.6 CJS, ESM and UMD bundles reference a missing file and cannot be imported directly; this source-built path is explicitly narrower. The tagged source, relevant files, npm tarball and control are hash pinned. Its 896 same-window downloads measure whole-package interest. GraphBox and keepset have the same publisher but separate parser implementations. Eleven paths remain below the working goal.
