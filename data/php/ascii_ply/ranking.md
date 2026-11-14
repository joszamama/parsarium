# PHP × ASCII PLY: verified parser ranking

One verified third-party package path; working goal 20, ceiling 30. The within-PHP metric is Packagist lifetime downloads across all releases, observed on 2026-11-14. It measures package adoption, not PLY-specific use. Nineteen paths remain below the goal; this one row does not establish a most-used top 20.

| Rank | Package | Pinned release | Packagist lifetime downloads | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [magdev/php-assimp](https://github.com/magdev/php-assimp/tree/0.3.2) | 0.3.2 | 94 | one mesh, three vertices, one face | Assimp 6.0.6 native PLY importer through PHP CLI wrapper |

The tagged MIT 0.3.2 release's `InfoVerb` appends the supplied local filename and invokes pinned Assimp 6.0.6. The PHP adapter read the wrapper's output and reported the control's mesh, vertex and face counts. This is a distinct PHP package path that shares Assimp's underlying parser family. The later 0.6.0 release was tested separately and remains excluded: its PHP result interface fails and its verb omits the input path. The wrapper does not escape shell arguments, so the verified replay is scoped to the repository's control path.

The bounded searches saved 50 exact Packagist and GitHub repository hits with 46 unique result identifiers. Three additional exact Sourcegraph searches over indexed `.php` files returned no PLY header or face terms; a positive control confirmed the file filter worked. These windows do not establish that no other PHP PLY parser exists. The PHP standard and bundled API inventory found no documented format-aware PLY parser within its stated scope. See `cell.json`, `supplementary-search.json`, `leads.json`, `source-lock.json`, `verification.json`, and `standard.json`.
