# C++ × Matrix Market: verified parser ranking

19 verified third-party package paths; working goal 20, ceiling 30. Homebrew install-on-request counts cover 2025-11-13 through 2026-11-13 and measure broad formula adoption, not Matrix Market-specific use. Compare only within C++.

| Rank | Package | Pinned release | Homebrew requested installs (365d) | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [eigen](https://libeigen.gitlab.io/eigen/docs-nightly/unsupported/group__SparseExtra__Module.html) | 5.0.1 | 16,505 | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | Eigen SparseExtra MarketIO |
| 2 | [suite-sparse](https://github.com/DrTimothyAldenDavis/SuiteSparse/blob/v7.14.1/CHOLMOD/Check/cholmod_read.c) | 7.14.1 | 10,821 | 2×3 real coordinate matrix and three nonzeros | SuiteSparse CHOLMOD Check reader |
| 3 | [SuperLU](https://github.com/xiaoyeli/superlu/blob/v7.0.1/SRC/dreadMM.c) | 7.0.1 | 333 | 3×3 symmetric matrix, three diagonal entries, entry (3,3) = 3 | SuperLU dreadMM reader lineage |
| 4 | [HYPRE](https://hypre.readthedocs.io/en/latest/api-int-ij.html) | 3.2.1 | 324 | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | HYPRE native IJ Matrix Market reader |
| 5 | [ginkgo](https://gko-project.org/user-guide/how-to/using/read-write-matrices.html) | 1.11.0 | 166 | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | Ginkgo native Matrix Market reader |
| 6 | [ViennaCL](https://viennacl.sourceforge.net/doc/iterative_8cpp-example.html) | 1.7.1 | 62 | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | ViennaCL native Matrix Market reader |
| unranked | [fast-matrix-market](https://github.com/alugowski/fast_matrix_market/blob/v1.7.6/README.md) | 1.7.6 | unknown | triplet dimensions, indices and entry (1,3) = −2 | fast_matrix_market native parser |
| unranked | [eminem](https://github.com/tatami-inc/eminem/blob/v1.2.3/README.md) | 1.2.3 | unknown | banner, dimensions and three real coordinate values | eminem Matrix Market parser |
| unranked | [lis](https://www.ssisc.org/lis/) | 2.1.23 | unknown | 3×3 symmetric matrix and three nonzeros | Lis native Matrix Market reader |
| unranked | [MTL5](https://github.com/stillwater-sc/mtl5/blob/v5.23.0/include/mtl/io/matrix_market.hpp) | 5.23.0 | unknown | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | MTL5 native Matrix Market reader |
| unranked | [LAGraph](https://lagraph.readthedocs.io/en/latest/utils.html) | 1.2.2 | unknown | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | LAGraph native Matrix Market reader |
| unranked | [librsb](https://librsb.sourceforge.net/doc/1.3.0.0/group__rsb__doc__rsb.html) | 1.3.0.3 | unknown | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | librsb native Matrix Market loader |
| unranked | [PIGO](https://github.com/GT-TDAlab/PIGO/blob/v0.6/tests/coo/test_weight_mtx.cpp) | 0.6 | unknown | three 1-based entries and value −2 at (1,3); reports dimensions 3×4 for a 2×3 file | PIGO native COO reader |
| unranked | [SuperLU_DIST](https://github.com/xiaoyeli/superlu_dist/blob/v9.3.0/README.md) | 9.3.0 | unknown | 3×3 symmetric matrix, three diagonal entries, entry (3,3) = 3 | SuperLU dreadMM reader lineage |
| unranked | [tatami_mtx](https://github.com/tatami-inc/tatami_mtx/blob/v2.1.2/README.md) | 2.1.2 | unknown | 2×3 real coordinate matrix and entry (1,3) = −2 | eminem Matrix Market parser |
| unranked | [Seldon](https://www.math.u-bordeaux.fr/~durufle/seldon/functions_matrix.html) | 5.2+ | unknown | 2×3 real general coordinate matrix and all three nonzero values | Seldon native Matrix Market reader |
| unranked | [HIFIR](https://hifirworks.github.io/hifir/group__io.html) | 0.2.0 | unknown | 2×3 real general coordinate matrix, three nonzeros, entry (1,3) = −2 | HIFIR native Matrix Market reader |
| unranked | [TACO](https://tensor-compiler.org/docs/tensors.html) | 0.1 | unknown | 2×3 real general coordinate matrix, three nonzeros, entry (1,3) = −2 | TACO native Matrix Market reader |
| unranked | [Trilinos Teuchos](https://trilinos.github.io/docs/teuchos/class_teuchos_1_1_matrix_market_1_1_raw_1_1_reader.html) | 17.3.0 | unknown | 2×3 real general coordinate matrix, three CSR entries, entry (1,3) = −2 | Trilinos Teuchos Matrix Market Raw reader |

Formula-name hits are leads rather than parser proof. The SuiteSparse and Lis paths each share an underlying parser with their C call sites. Lis accepts the square symmetric control and rejects the rectangular general control. The C++ standard library has no documented Matrix Market parser. See `cell.json`, `leads.json`, `source-lock.json`, and `verification.json`.

ViennaCL 1.7.1 uses its documented local-file reader with a host sparse matrix adapter. The release and installed headers are hash-pinned; the 62 requested installs use the same Homebrew 365-day window as the ranked packages.

MTL5 5.23.0 is a tagged MIT header-only C++20 reader. Its valid local-file control passed; it has no comparable Homebrew requested-install metric and remains unranked.

HYPRE 3.2.1 parsed the valid local Matrix Market control through `HYPRE_IJMatrixReadMM`. Its C and C++ call sites share one native parser family; 324 requested installs use the same Homebrew 365-day window as the other ranked packages.

LAGraph 1.2.2 parsed the local Matrix Market control through `LAGraph_MMRead(FILE *)`. Its C and C++ adapters share the LAGraph reader, backed by SuiteSparse GraphBLAS for matrix storage. The reader is distinct from CHOLMOD Check. LAGraph has no comparable Homebrew requested-install count and remains unranked.

librsb 1.3.0.3 parsed the control through `rsb_file_mtx_load(local filename)`. Its C and C++ adapters share one native reader. The official LGPL-3.0-or-later release is source-pinned and built locally; no comparable Homebrew requested-install count was available.

SuperLU 7.0.1 parsed the valid square symmetric control through `dreadMM(FILE *)`. Its source rejects rectangular matrices. The C and C++ adapters share one native reader; 333 Homebrew requested installs are recorded in the same 365-day window.

PIGO v0.6 parsed the three weighted coordinate entries in the valid 2×3 real general control. Its API reported `nrows=3` and `ncols=4`, one greater than the header in both cases; the adapter reports those raw values. No comparable Homebrew requested-install count is available, so PIGO remains unranked.

SuperLU_DIST 9.3.0 parsed the valid square control through `dreadMM_dist(FILE *)`. It is a separate released package and build whose reader shares the SuperLU dreadMM lineage. Its C and C++ adapters share one native implementation. No comparable Homebrew requested-install count is available, so it remains unranked.

tatami_mtx 2.1.2 parsed the valid 2×3 control through `load_matrix_from_text_file`. It adds a tatami matrix wrapper around eminem and shares that underlying parser. All five tagged header dependencies are pinned. No comparable Homebrew requested-install count is available, so it remains unranked.

Seldon 5.2+ parsed the local control through `ReadMatrixMarket(filename, Matrix&)`. The author-hosted URL is labeled latest release and can change, so the exact 714 KiB LGPL source archive is included under `sources/` and hash-pinned. The extracted release reports `5.2+` in its version file. No comparable Homebrew requested-install count exists; Seldon remains unranked.

HIFIR v0.2.0 parsed the control with `read_mm_sparse(local filename, …)` and exposed the three zero-based coordinate entries. It is an independent AGPL-3.0-or-later C++ release. No comparable Homebrew requested-install count exists; HIFIR remains unranked.

TACO v0.1 parsed the control with `taco::read(local .mtx filename, Sparse)` into a sparse tensor. The official GitHub API showed 1,380 repository stars on 2026-11-13; this is an auxiliary adoption signal and is not comparable with the Homebrew requested-install counts in the primary ranking. TACO remains unranked in that table.

Trilinos 17.3.0 parsed the control with Teuchos `Raw::Reader::readFile`, returning three CSR entries. Its Teuchos component was built from the official release and linked locally. The official GitHub API showed 1,444 repository stars on 2026-11-13; this auxiliary adoption signal is not compared with Homebrew requested installs. Trilinos remains unranked in the primary table.
