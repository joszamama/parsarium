# C × Matrix Market: verified parser ranking

9 verified third-party package paths; working goal 20, ceiling 30. Homebrew install-on-request counts cover 2025-11-13 through 2026-11-13 and measure broad formula adoption, not Matrix Market-specific use. Compare only within C.

| Rank | Package | Pinned release | Homebrew requested installs (365d) | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [suite-sparse](https://github.com/DrTimothyAldenDavis/SuiteSparse/blob/v7.14.1/CHOLMOD/Check/cholmod_read.c) | 7.14.1 | 10,821 | 2×3 real coordinate matrix and three nonzeros | SuiteSparse CHOLMOD Check reader |
| 2 | [GNU GSL](https://www.gnu.org/software/gsl/doc/html/spmatrix.html) | 2.8 | 5,333 | 2×3 real general coordinate matrix, three nonzeros, entry (1,3) = −2 | GNU GSL sparse Matrix Market reader |
| 3 | [SuperLU](https://github.com/xiaoyeli/superlu/blob/v7.0.1/SRC/dreadMM.c) | 7.0.1 | 333 | 3×3 symmetric matrix, three diagonal entries, entry (3,3) = 3 | SuperLU dreadMM reader lineage |
| 4 | [HYPRE](https://hypre.readthedocs.io/en/latest/api-int-ij.html) | 3.2.1 | 324 | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | HYPRE native IJ Matrix Market reader |
| unranked | [lis](https://www.ssisc.org/lis/) | 2.1.23 | unknown | 3×3 symmetric matrix and three nonzeros | Lis native Matrix Market reader |
| unranked | [LAGraph](https://lagraph.readthedocs.io/en/latest/utils.html) | 1.2.2 | unknown | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | LAGraph native Matrix Market reader |
| unranked | [librsb](https://librsb.sourceforge.net/doc/1.3.0.0/group__rsb__doc__rsb.html) | 1.3.0.3 | unknown | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | librsb native Matrix Market loader |
| unranked | [BeBOP SMC](https://bebop.cs.berkeley.edu/smc/features.html) | 2009-12-11 dated source | unknown | 2×3 real coordinate matrix, three entries, value (1,3) = −2 | BeBOP reader with bundled NIST mmio banner parser |
| unranked | [SuperLU_DIST](https://github.com/xiaoyeli/superlu_dist/blob/v9.3.0/README.md) | 9.3.0 | unknown | 3×3 symmetric matrix, three diagonal entries, entry (3,3) = 3 | SuperLU dreadMM reader lineage |

Formula-name hits are leads rather than parser proof. The C standard library has no documented Matrix Market parser. C and C++ call sites share the CHOLMOD and Lis parser families. Lis accepts the square symmetric control and rejects the rectangular general control. See `cell.json`, `leads.json`, `source-lock.json`, and `verification.json`.

HYPRE 3.2.1 parsed the valid local Matrix Market control through `HYPRE_IJMatrixReadMM`. Its C and C++ call sites share one native parser family; 324 requested installs use the same Homebrew 365-day window as SuiteSparse.

LAGraph 1.2.2 parsed the local Matrix Market control through `LAGraph_MMRead(FILE *)`. Its C and C++ adapters share the LAGraph reader, which uses SuiteSparse GraphBLAS for matrix storage. The reader is distinct from CHOLMOD Check. LAGraph has no comparable Homebrew requested-install count and remains unranked.

librsb 1.3.0.3 parsed the control through `rsb_file_mtx_load(local filename)`. Its C and C++ adapters share one native reader. The official LGPL-3.0-or-later release is source-pinned and built locally; no comparable Homebrew requested-install count was available.

SuperLU 7.0.1 parsed the valid square symmetric control through `dreadMM(FILE *)`. Its source rejects rectangular matrices. The C and C++ adapters share one native reader; 333 Homebrew requested installs are recorded in the same 365-day window.

SuperLU_DIST 9.3.0 parsed the same valid square control through `dreadMM_dist(FILE *)`. It is a separate released package and build whose reader shares the SuperLU dreadMM lineage. Its C and C++ adapters share one native implementation. No comparable Homebrew requested-install count is available, so it remains unranked.

GNU GSL 2.8 parsed the valid control with `gsl_spmatrix_fscanf(FILE *)` in both C and C++ call sites. The calls share one underlying reader. Its 5,333 Homebrew requested installs are comparable with the other ranked formulae in this ecosystem. The source skips the banner line rather than validating it; the demonstrated scope is real general coordinate input.

BeBOP SMC is an official dated BSD source release with a local C API. It passed the control and remains unranked because its source distribution has no comparable Homebrew requested-install count.
