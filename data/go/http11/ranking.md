# GO × HTTP/1.1: selected parsers

10 control-verified third-party paths selected from 21 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

pkg.go.dev Imported by package count.

| Rank | Package | Release | Imported by (pkg.go.dev) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/valyala/fasthttp](https://pkg.go.dev/github.com/valyala/fasthttp@v1.78.0) | v1.78.0 | 9,851 | request message | fasthttp HTTP/1 parser |
| 2 | [github.com/gobwas/httphead](https://pkg.go.dev/github.com/gobwas/httphead@v0.1.0) | v0.1.0 | 145 | request line only | gobwas HTTP request-line parser |
| 3 | [github.com/lesismal/nbio/nbhttp](https://pkg.go.dev/github.com/lesismal/nbio/nbhttp@v1.7.1) | v1.7.1 | 72 | request message | nbio HTTP parser |
| 4 | [github.com/evanphx/wildcat](https://pkg.go.dev/github.com/evanphx/wildcat@v0.0.0-20141114174135-e7012f664567) | v0.0.0-20141114174135-e7012f664567 | 16 | request head | wildcat HTTP parser |
| 5 | [gnalloy.org/codec-http1](https://pkg.go.dev/gnalloy.org/codec-http1@v0.0.0-20261006130159-161e7f51078b) | v0.0.0-20261006130159-161e7f51078b | 5 | request message | gnalloy codec-http1 parser |
| 6 | [github.com/cloudwego/hertz/pkg/protocol/http1/req](https://pkg.go.dev/github.com/cloudwego/hertz/pkg/protocol/http1/req@v0.10.6) | v0.10.6 | 4 | request message | Hertz / fasthttp lineage |
| 7 | [github.com/lemon4ksan/mach/server/h1](https://pkg.go.dev/github.com/lemon4ksan/mach/server/h1@v0.2.0) | v0.2.0 | 3 | request message | mach H1 parser |
| 8 | [github.com/projectdiscovery/nuclei/v3/pkg/protocols/http/raw](https://pkg.go.dev/github.com/projectdiscovery/nuclei/v3/pkg/protocols/http/raw@v3.11.1) | v3.11.1 | 2 | raw request message | nuclei raw HTTP parser |
| 9 | [github.com/antlabs/httparser](https://pkg.go.dev/github.com/antlabs/httparser@v0.0.11) | v0.0.11 | 1 | request message | antlabs httparser |
| 10 | [github.com/hsiafan/httpdump/httpport](https://pkg.go.dev/github.com/hsiafan/httpdump/httpport@v0.0.0-20231019014708-4fd809447b59) | v0.0.0-20231019014708-4fd809447b59 | 1 | request message | Go net/http port |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
