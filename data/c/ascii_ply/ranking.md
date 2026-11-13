# C × ASCII PLY: verified parser ranking

4 verified third-party package paths; working goal 20, ceiling 30. Homebrew install-on-request counts cover 2025-11-13 through 2026-11-13 and measure broad formula adoption, not PLY-specific use. They are compared only within this ecosystem.

| Rank | Package | Pinned release | Homebrew requested installs (365d) | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [assimp](https://github.com/assimp/assimp-docs/blob/master/source/usage/use_the_lib.rst) | 6.0.6 | 7,646 | three vertices, one face | Assimp native PLY loader |
| unranked | [RPly](https://w3.impa.br/~diego/software/rply/) | 1.1.4 | unknown | vertex and face-index callbacks | RPly ANSI C parser |
| unranked | [SPly](https://github.com/Anteru/sply/blob/1.2.0/Readme.md) | 1.2.0 | unknown | three vertices and a parsed triangle face | SPly fork of RPly parser |
| unranked | [AssetKit](https://github.com/recp/AssetKit/blob/v0.7.4/samples/read_meshes.c) | 0.7.4 | unknown | mesh vertices and parsed face indices | AssetKit native ASCII PLY importer |

Assimp C and C++ entry points share one native loader; RPly has its own C parser and a C++ callable API; SPly is a separately released fork of the same parser lineage. The search results include fuzzy names and unresolved leads; a registry hit alone is not proof of format parsing. See `cell.json`, `leads.json`, `source-lock.json`, and `verification.json`.

AssetKit v0.7.4 was verified through its local `ak_load` API in both C and C++. Both adapters share one native PLY parser family. Its tagged source, five submodule commits, and adapter control results are pinned; a comparable Homebrew install-on-request count is unavailable.

SPly 1.2.0 was verified from its tagged MIT source. Its three GitHub stars are an auxiliary project-interest signal; no comparable Homebrew formula metric exists, so its popularity order remains unresolved.
