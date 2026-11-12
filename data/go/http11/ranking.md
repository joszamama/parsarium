# Go × HTTP/1.1: verified parser ranking

20 verified third-party packages; working goal 20, original ceiling 30. The metric is pkg.go.dev's package-level ‘Imported by’ count captured at 2026-11-11T19:02:25.648350+00:00. It measures visible direct importers rather than downloads, and is used only within Go. 0 package(s) lack a metric and remain unranked; equal counts share a rank.

Search hits and unresolved leads are separate from this ranking. See `cell.json`, `registry-snapshot.json`, and `verification.json` in this directory.

| Rank | Package | Pinned module release | Imported by packages | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/valyala/fasthttp](https://pkg.go.dev/github.com/valyala/fasthttp@v1.78.0) | github.com/valyala/fasthttp@v1.78.0 | 9,851 | request message | fasthttp HTTP/1 parser |
| 2 | [github.com/gobwas/httphead](https://pkg.go.dev/github.com/gobwas/httphead@v0.1.0) | github.com/gobwas/httphead@v0.1.0 | 145 | request line only | gobwas HTTP request-line parser |
| 3 | [github.com/lesismal/nbio/nbhttp](https://pkg.go.dev/github.com/lesismal/nbio/nbhttp@v1.7.1) | github.com/lesismal/nbio@v1.7.1 | 72 | request message | nbio HTTP parser |
| 4 | [github.com/evanphx/wildcat](https://pkg.go.dev/github.com/evanphx/wildcat@v0.0.0-20141114174135-e7012f664567) | github.com/evanphx/wildcat@v0.0.0-20141114174135-e7012f664567 | 16 | request head | wildcat HTTP parser |
| 5 | [github.com/cloudwego/hertz/pkg/protocol/http1/req](https://pkg.go.dev/github.com/cloudwego/hertz/pkg/protocol/http1/req@v0.10.6) | github.com/cloudwego/hertz@v0.10.6 | 4 | request message | Hertz / fasthttp lineage |
| 6 | [github.com/lemon4ksan/mach/server/h1](https://pkg.go.dev/github.com/lemon4ksan/mach/server/h1@v0.2.0) | github.com/lemon4ksan/mach@v0.2.0 | 3 | request message | mach H1 parser |
| 7 | [github.com/projectdiscovery/nuclei/v3/pkg/protocols/http/raw](https://pkg.go.dev/github.com/projectdiscovery/nuclei/v3/pkg/protocols/http/raw@v3.11.1) | github.com/projectdiscovery/nuclei/v3@v3.11.1 | 2 | raw request message | nuclei raw HTTP parser |
| 8 | [github.com/antlabs/httparser](https://pkg.go.dev/github.com/antlabs/httparser@v0.0.11) | github.com/antlabs/httparser@v0.0.11 | 1 | request message | antlabs httparser |
| 8 | [github.com/hsiafan/httpdump/httpport](https://pkg.go.dev/github.com/hsiafan/httpdump/httpport@v0.0.0-20231019014708-4fd809447b59) | github.com/hsiafan/httpdump@v0.0.0-20231019014708-4fd809447b59 | 1 | request message | Go net/http port |
| 10 | [github.com/FastTLS/oohttp](https://pkg.go.dev/github.com/FastTLS/oohttp@v0.0.0-20261026180050-43186effd7f4) | github.com/FastTLS/oohttp@v0.0.0-20261026180050-43186effd7f4 | 0 | request message | Go net/http fork |
| 10 | [github.com/antlabs/fio/http](https://pkg.go.dev/github.com/antlabs/fio/http@v0.2.8) | github.com/antlabs/fio@v0.2.8 | 0 | request message | fio native HTTP parser |
| 10 | [github.com/go-fasthttp/fasthttp](https://pkg.go.dev/github.com/go-fasthttp/fasthttp@v0.0.0-20161128095036-1c39678a4dd0) | github.com/go-fasthttp/fasthttp@v0.0.0-20161128095036-1c39678a4dd0 | 0 | request message | fasthttp HTTP/1 parser |
| 10 | [github.com/hellpuffyt/spindrift/http1](https://pkg.go.dev/github.com/hellpuffyt/spindrift/http1) | github.com/hellpuffyt/spindrift@v0.0.0-20261022160824-5a92c9177f42 | 0 | request message | spindrift HTTP/1 parser |
| 10 | [github.com/justIliane/blazehttp/pkg/header](https://pkg.go.dev/github.com/justIliane/blazehttp/pkg/header@v1.0.0) | github.com/justIliane/blazehttp@v1.0.0 | 0 | request header | blazehttp header parser |
| 10 | [github.com/lesismal/fib/http](https://pkg.go.dev/github.com/lesismal/fib/http@v1.5.6) | github.com/lesismal/fib@v1.5.6 | 0 | request message | fib HTTP parser |
| 10 | [github.com/meta-apex/metarpc/codec/http](https://pkg.go.dev/github.com/meta-apex/metarpc/codec/http@v0.0.0-20250816075809-78e603aff299) | github.com/meta-apex/metarpc@v0.0.0-20250816075809-78e603aff299 | 0 | request message | fasthttp-derived metarpc parser |
| 10 | [github.com/nelthaarion/breeze](https://pkg.go.dev/github.com/nelthaarion/breeze@v1.6.2) | github.com/nelthaarion/breeze@v1.6.2 | 0 | request message | breeze HTTP parser |
| 10 | [github.com/openctemio/openctem/api/pkg/domain/evidence](https://pkg.go.dev/github.com/openctemio/openctem/api/pkg/domain/evidence@v0.0.0-20261107202920-27e7faec6f5d) | github.com/openctemio/openctem/api@v0.0.0-20261107202920-27e7faec6f5d | 0 | raw request message | openctem raw HTTP parser |
| 10 | [github.com/sebishogun/simdhttp/http1](https://pkg.go.dev/github.com/sebishogun/simdhttp/http1@v0.0.0-20261007210108-01268e016029) | github.com/sebishogun/simdhttp@v0.0.0-20261007210108-01268e016029 | 0 | request head | simdhttp HTTP/1 parser |
| 10 | [github.com/zhaofenghao/clash/listener/http](https://pkg.go.dev/github.com/zhaofenghao/clash/listener/http@v1.0.14) | github.com/zhaofenghao/clash@v1.0.14 | 0 | request message | Go net/http fork or wrapper |
