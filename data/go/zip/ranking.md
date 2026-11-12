# Go × ZIP: verified parser ranking

23 verified third-party packages; working goal 20, original ceiling 30. The metric is pkg.go.dev's package-level ‘Imported by’ count captured at 2026-11-11T18:21:27.062372+00:00. It measures visible direct importers rather than downloads, and is used only within Go. 0 package(s) lack a metric and remain unranked; equal counts share a rank.

Search hits and unresolved leads are separate from this ranking. See `cell.json`, `registry-snapshot.json`, and `verification.json` in this directory.

| Rank | Package | Pinned module release | Imported by packages | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/klauspost/compress/zip](https://pkg.go.dev/github.com/klauspost/compress/zip@v1.20.4) | github.com/klauspost/compress@v1.20.4 | 246 | entry_name+decompressed_text | Go archive/zip fork |
| 2 | [github.com/mholt/archives](https://pkg.go.dev/github.com/mholt/archives@v0.1.5) | github.com/mholt/archives@v0.1.5 | 228 | entry_name+decompressed_text | mholt/archives/STARRY-S zip |
| 3 | [github.com/daaku/go.zipexe](https://pkg.go.dev/github.com/daaku/go.zipexe@v1.0.2) | github.com/daaku/go.zipexe@v1.0.2 | 207 | entry_name+decompressed_text | Go archive/zip wrapper |
| 4 | [github.com/evilsocket/islazy/zip](https://pkg.go.dev/github.com/evilsocket/islazy/zip@v1.11.0) | github.com/evilsocket/islazy@v1.11.0 | 113 | entry_name+decompressed_text | Go archive/zip wrapper |
| 5 | [github.com/yeka/zip](https://pkg.go.dev/github.com/yeka/zip@v0.0.0-20231116150916-03d6312748a9) | github.com/yeka/zip@v0.0.0-20231116150916-03d6312748a9 | 108 | entry_name+decompressed_text | yeka/alexmullins ZIP lineage |
| 6 | [github.com/alexmullins/zip](https://pkg.go.dev/github.com/alexmullins/zip@v0.0.0-20180717182244-4affb64b04d0) | github.com/alexmullins/zip@v0.0.0-20180717182244-4affb64b04d0 | 92 | entry_name+decompressed_text | yeka/alexmullins ZIP lineage |
| 7 | [code.cloudfoundry.org/ykk](https://pkg.go.dev/code.cloudfoundry.org/ykk@v0.0.0-20170424192843-e4df4ce2fd4d) | code.cloudfoundry.org/ykk@v0.0.0-20170424192843-e4df4ce2fd4d | 79 | entry_name+decompressed_text | Go archive/zip wrapper |
| 8 | [github.com/gen2brain/go-unarr](https://pkg.go.dev/github.com/gen2brain/go-unarr@v0.2.4) | github.com/gen2brain/go-unarr@v0.2.4 | 48 | entry_name+decompressed_text | unarr archive backend |
| 9 | [github.com/c4milo/unpackit](https://pkg.go.dev/github.com/c4milo/unpackit@v1.0.0) | github.com/c4milo/unpackit@v1.0.0 | 40 | entry_name+decompressed_text | Go archive/zip wrapper |
| 10 | [github.com/pierrre/archivefile/zip](https://pkg.go.dev/github.com/pierrre/archivefile/zip@v0.0.0-20170218184037-e2d100bc74f5) | github.com/pierrre/archivefile@v0.0.0-20170218184037-e2d100bc74f5 | 39 | entry_name+decompressed_text | Go archive/zip wrapper |
| 11 | [github.com/krolaw/zipstream](https://pkg.go.dev/github.com/krolaw/zipstream) | github.com/krolaw/zipstream@v0.0.0-20241109034754-4a67be70fe31 | 36 | entry_name+decompressed_text | zipstream |
| 12 | [github.com/codeclysm/extract/v4](https://pkg.go.dev/github.com/codeclysm/extract/v4@v4.0.2) | github.com/codeclysm/extract/v4@v4.0.2 | 12 | entry_name+decompressed_text | Go archive/zip wrapper |
| 13 | [github.com/STARRY-S/zip](https://pkg.go.dev/github.com/STARRY-S/zip@v0.2.3) | github.com/STARRY-S/zip@v0.2.3 | 10 | entry_name+decompressed_text | Go archive/zip fork |
| 13 | [github.com/xyproto/unzip](https://pkg.go.dev/github.com/xyproto/unzip@v1.0.1) | github.com/xyproto/unzip@v1.0.1 | 10 | entry_name+decompressed_text | Go archive/zip wrapper |
| 15 | [github.com/unknwon/cae/zip](https://pkg.go.dev/github.com/unknwon/cae/zip@v1.0.2) | github.com/unknwon/cae@v1.0.2 | 8 | entry_name+decompressed_text | Go archive/zip wrapper |
| 16 | [github.com/nmiyake/archiver](https://pkg.go.dev/github.com/nmiyake/archiver@v1.1.1) | github.com/nmiyake/archiver@v1.1.1 | 7 | entry_name+decompressed_text | mholt/archiver fork |
| 17 | [github.com/andrewarchi/archive](https://pkg.go.dev/github.com/andrewarchi/archive@v0.0.0-20210213193640-3a6449eed2ec) | github.com/andrewarchi/archive@v0.0.0-20210213193640-3a6449eed2ec | 4 | entry_name+decompressed_text | Go archive/zip wrapper |
| 17 | [github.com/git-pkgs/archives](https://pkg.go.dev/github.com/git-pkgs/archives@v0.11.0) | github.com/git-pkgs/archives@v0.11.0 | 4 | entry_name+decompressed_text | Go archive/zip wrapper |
| 17 | [github.com/google/safearchive/zip](https://pkg.go.dev/github.com/google/safearchive/zip@v0.0.0-20241025131057-f7ce9d7b6f9c) | github.com/google/safearchive@v0.0.0-20241025131057-f7ce9d7b6f9c | 4 | entry_name+decompressed_text | Go archive/zip fork |
| 17 | [github.com/hillu/go-archive-zip-crypto](https://pkg.go.dev/github.com/hillu/go-archive-zip-crypto@v0.0.0-20200712202847-bd5cf365dd44) | github.com/hillu/go-archive-zip-crypto@v0.0.0-20200712202847-bd5cf365dd44 | 4 | entry_name+decompressed_text | Go archive/zip fork |
| 21 | [github.com/sagan/zip](https://pkg.go.dev/github.com/sagan/zip@v0.0.0-20240708090818-02b11188bf71) | github.com/sagan/zip@v0.0.0-20240708090818-02b11188bf71 | 2 | entry_name+decompressed_text | yeka/alexmullins ZIP lineage |
| 22 | [github.com/sourcegraph/lazyzip](https://pkg.go.dev/github.com/sourcegraph/lazyzip@v0.0.0-20180104141618-672a4b512c09) | github.com/sourcegraph/lazyzip@v0.0.0-20180104141618-672a4b512c09 | 0 | entry_name+decompressed_text | Go archive/zip fork |
| 22 | [github.com/unxed/zip](https://pkg.go.dev/github.com/unxed/zip@v0.1.146) | github.com/unxed/zip@v0.1.146 | 0 | entry_name+decompressed_text | unxed ZIP |
