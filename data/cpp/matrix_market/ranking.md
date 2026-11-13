# C++ × Matrix Market: verified parser ranking

5 verified third-party package paths; working goal 20, ceiling 30. Homebrew install-on-request counts cover 2025-11-13 through 2026-11-13 and measure broad formula adoption, not Matrix Market-specific use. Compare only within C++.

| Rank | Package | Pinned release | Homebrew requested installs (365d) | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [eigen](https://libeigen.gitlab.io/eigen/docs-nightly/unsupported/group__SparseExtra__Module.html) | 5.0.1 | 16,505 | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | Eigen SparseExtra MarketIO |
| 2 | [suite-sparse](https://github.com/DrTimothyAldenDavis/SuiteSparse/blob/v7.14.1/CHOLMOD/Check/cholmod_read.c) | 7.14.1 | 10,821 | 2×3 real coordinate matrix and three nonzeros | SuiteSparse CHOLMOD Check reader |
| 3 | [ginkgo](https://gko-project.org/user-guide/how-to/using/read-write-matrices.html) | 1.11.0 | 166 | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | Ginkgo native Matrix Market reader |
| unranked | [fast-matrix-market](https://github.com/alugowski/fast_matrix_market/blob/v1.7.6/README.md) | 1.7.6 | unknown | triplet dimensions, indices and entry (1,3) = −2 | fast_matrix_market native parser |
| unranked | [eminem](https://github.com/tatami-inc/eminem/blob/v1.2.3/README.md) | 1.2.3 | unknown | banner, dimensions and three real coordinate values | eminem native parser over byteme input |

Formula-name hits are leads rather than parser proof. The SuiteSparse path shares CHOLMOD with C. The C++ standard library has no documented Matrix Market parser. See `cell.json`, `leads.json`, `source-lock.json`, and `verification.json`.
