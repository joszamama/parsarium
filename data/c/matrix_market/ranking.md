# C × Matrix Market: verified parser ranking

2 verified third-party package paths; working goal 20, ceiling 30. Homebrew install-on-request counts cover 2025-11-13 through 2026-11-13 and measure broad formula adoption, not Matrix Market-specific use. Compare only within C.

| Rank | Package | Pinned release | Homebrew requested installs (365d) | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [suite-sparse](https://github.com/DrTimothyAldenDavis/SuiteSparse/blob/v7.14.1/CHOLMOD/Check/cholmod_read.c) | 7.14.1 | 10,821 | 2×3 real coordinate matrix and three nonzeros | SuiteSparse CHOLMOD Check reader |
| unranked | [lis](https://www.ssisc.org/lis/) | 2.1.23 | unknown | 3×3 symmetric matrix and three nonzeros | Lis native Matrix Market reader |

Formula-name hits are leads rather than parser proof. The C standard library has no documented Matrix Market parser. C and C++ call sites share the CHOLMOD and Lis parser families. Lis accepts the square symmetric control and rejects the rectangular general control. See `cell.json`, `leads.json`, `source-lock.json`, and `verification.json`.
