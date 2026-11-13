# C++ × Matrix Market: verified parser ranking

9 verified third-party package paths; working goal 20, ceiling 30. Homebrew install-on-request counts cover 2025-11-13 through 2026-11-13 and measure broad formula adoption, not Matrix Market-specific use. Compare only within C++.

| Rank | Package | Pinned release | Homebrew requested installs (365d) | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [eigen](https://libeigen.gitlab.io/eigen/docs-nightly/unsupported/group__SparseExtra__Module.html) | 5.0.1 | 16,505 | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | Eigen SparseExtra MarketIO |
| 2 | [suite-sparse](https://github.com/DrTimothyAldenDavis/SuiteSparse/blob/v7.14.1/CHOLMOD/Check/cholmod_read.c) | 7.14.1 | 10,821 | 2×3 real coordinate matrix and three nonzeros | SuiteSparse CHOLMOD Check reader |
| 3 | [HYPRE](https://hypre.readthedocs.io/en/latest/api-int-ij.html) | 3.2.1 | 324 | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | HYPRE native IJ Matrix Market reader |
| 4 | [ginkgo](https://gko-project.org/user-guide/how-to/using/read-write-matrices.html) | 1.11.0 | 166 | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | Ginkgo native Matrix Market reader |
| 5 | [ViennaCL](https://viennacl.sourceforge.net/doc/iterative_8cpp-example.html) | 1.7.1 | 62 | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | ViennaCL native Matrix Market reader |
| unranked | [fast-matrix-market](https://github.com/alugowski/fast_matrix_market/blob/v1.7.6/README.md) | 1.7.6 | unknown | triplet dimensions, indices and entry (1,3) = −2 | fast_matrix_market native parser |
| unranked | [eminem](https://github.com/tatami-inc/eminem/blob/v1.2.3/README.md) | 1.2.3 | unknown | banner, dimensions and three real coordinate values | eminem native parser over byteme input |
| unranked | [lis](https://www.ssisc.org/lis/) | 2.1.23 | unknown | 3×3 symmetric matrix and three nonzeros | Lis native Matrix Market reader |
| unranked | [MTL5](https://github.com/stillwater-sc/mtl5/blob/v5.23.0/include/mtl/io/matrix_market.hpp) | 5.23.0 | unknown | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | MTL5 native Matrix Market reader |

Formula-name hits are leads rather than parser proof. The SuiteSparse and Lis paths each share an underlying parser with their C call sites. Lis accepts the square symmetric control and rejects the rectangular general control. The C++ standard library has no documented Matrix Market parser. See `cell.json`, `leads.json`, `source-lock.json`, and `verification.json`.

ViennaCL 1.7.1 uses its documented local-file reader with a host sparse matrix adapter. The release and installed headers are hash-pinned; the 62 requested installs use the same Homebrew 365-day window as the ranked packages.

MTL5 5.23.0 is a tagged MIT header-only C++20 reader. Its valid local-file control passed; it has no comparable Homebrew requested-install metric and remains unranked.

HYPRE 3.2.1 parsed the valid local Matrix Market control through `HYPRE_IJMatrixReadMM`. Its C and C++ call sites share one native parser family; 324 requested installs use the same Homebrew 365-day window as the other ranked packages.
