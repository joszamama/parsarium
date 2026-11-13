# C × Matrix Market: verified parser ranking

6 verified third-party package paths; working goal 20, ceiling 30. Homebrew install-on-request counts cover 2025-11-13 through 2026-11-13 and measure broad formula adoption, not Matrix Market-specific use. Compare only within C.

| Rank | Package | Pinned release | Homebrew requested installs (365d) | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [suite-sparse](https://github.com/DrTimothyAldenDavis/SuiteSparse/blob/v7.14.1/CHOLMOD/Check/cholmod_read.c) | 7.14.1 | 10,821 | 2×3 real coordinate matrix and three nonzeros | SuiteSparse CHOLMOD Check reader |
| 2 | [SuperLU](https://github.com/xiaoyeli/superlu/blob/v7.0.1/SRC/dreadMM.c) | 7.0.1 | 333 | 3×3 symmetric matrix, three diagonal entries, entry (3,3) = 3 | SuperLU native dreadMM reader |
| 3 | [HYPRE](https://hypre.readthedocs.io/en/latest/api-int-ij.html) | 3.2.1 | 324 | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | HYPRE native IJ Matrix Market reader |
| unranked | [lis](https://www.ssisc.org/lis/) | 2.1.23 | unknown | 3×3 symmetric matrix and three nonzeros | Lis native Matrix Market reader |
| unranked | [LAGraph](https://lagraph.readthedocs.io/en/latest/utils.html) | 1.2.2 | unknown | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | LAGraph native Matrix Market reader |
| unranked | [librsb](https://librsb.sourceforge.net/doc/1.3.0.0/group__rsb__doc__rsb.html) | 1.3.0.3 | unknown | 2×3 real coordinate matrix, three nonzeros, entry (1,3) = −2 | librsb native Matrix Market loader |

Formula-name hits are leads rather than parser proof. The C standard library has no documented Matrix Market parser. C and C++ call sites share the CHOLMOD and Lis parser families. Lis accepts the square symmetric control and rejects the rectangular general control. See `cell.json`, `leads.json`, `source-lock.json`, and `verification.json`.

HYPRE 3.2.1 parsed the valid local Matrix Market control through `HYPRE_IJMatrixReadMM`. Its C and C++ call sites share one native parser family; 324 requested installs use the same Homebrew 365-day window as SuiteSparse.

LAGraph 1.2.2 parsed the local Matrix Market control through `LAGraph_MMRead(FILE *)`. Its C and C++ adapters share the LAGraph reader, which uses SuiteSparse GraphBLAS for matrix storage. The reader is distinct from CHOLMOD Check. LAGraph has no comparable Homebrew requested-install count and remains unranked.

librsb 1.3.0.3 parsed the control through `rsb_file_mtx_load(local filename)`. Its C and C++ adapters share one native reader. The official LGPL-3.0-or-later release is source-pinned and built locally; no comparable Homebrew requested-install count was available.

SuperLU 7.0.1 parsed the valid square symmetric control through `dreadMM(FILE *)`. Its source rejects rectangular matrices. The C and C++ adapters share one native reader; 333 Homebrew requested installs are recorded in the same 365-day window.
