# C × ASCII PLY: verified parser ranking

1 verified third-party package path; working goal 20, ceiling 30. Homebrew install-on-request counts cover 2025-11-13 through 2026-11-13 and measure broad formula adoption, not PLY-specific use. They are compared only within this ecosystem.

| Rank | Package | Pinned release | Homebrew requested installs (365d) | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [assimp](https://github.com/assimp/assimp-docs/blob/master/source/usage/use_the_lib.rst) | 6.0.6 | 7,646 | three vertices, one face | Assimp native PLY loader |

Assimp C and C++ entry points share the same underlying loader. OpenMesh has a distinct PLY reader. The search results include fuzzy names and unresolved leads; a registry hit alone is not proof of format parsing. See `cell.json`, `leads.json`, `source-lock.json`, and `verification.json`.
