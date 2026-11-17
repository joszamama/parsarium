# GO × TOML: selected parsers (pilot)

3 control-verified third-party paths selected. The ceiling is ten; ranks cover only verified paths from the bounded search. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

pkg.go.dev Imported by package count, from the bounded search captured 2026-11-17 ([snapshot](registry-snapshot.json)).

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [github.com/BurntSushi/toml](https://pkg.go.dev/github.com/BurntSushi/toml@v1.6.0#Decode) | v1.6.0 | 38,240 | TOML 1.0.0 document decoded into map[string]any; local date-times, dates and times are time.Time values in the fixed zones datetime-local, date-local and time-local | BurntSushi/toml lexer and parser |
| 2 | [github.com/pelletier/go-toml/v2](https://pkg.go.dev/github.com/pelletier/go-toml/v2@v2.4.3#Unmarshal) | v2.4.3 | 1,986 | TOML 1.0.0 document decoded into map[string]any; local date-times, dates and times are toml.LocalDateTime, toml.LocalDate and toml.LocalTime values and offset date-times are time.Time | go-toml v2 (pelletier) unstable.Parser |
| 3 | [github.com/go-rotini/toml](https://pkg.go.dev/github.com/go-rotini/toml@v1.2.2#Unmarshal) | v1.2.2 | 2 | TOML 1.0.0 document decoded into map[string]any; local date-times, dates and times are toml.LocalDateTime, toml.LocalDate and toml.LocalTime values and offset date-times are time.Time | go-rotini/toml scanner and parser |

The Go 1.27.1 standard library has no TOML package ([standard.json](standard.json)).

Each path decodes both valid controls into the exact typed tree of `catalog/toml/PROTOCOL.md`. BurntSushi/toml runs its own state-function lexer (`lex.go`) and parser (`parse.go`); go-toml v2 runs its own `unstable/parser.go` and decoder; go-rotini/toml runs its own `scanner.go`, `parser.go` node tree and `decode.go`. They share no code: of go-rotini/toml's 2,897 distinct non-test source lines, 121 also occur in BurntSushi/toml and 148 in go-toml v2, all generic Go statements. AFL++ feedback is scoped to each module's Go cover blocks; three repeats per control are identical, and the controls differ by 169 tuples (BurntSushi), 342 tuples (go-toml v2) and 240 tuples (go-rotini) ([afl-feedback.json](afl-feedback.json)). go-rotini/toml covers 720 own lines on service-config and 790 on typed-scalars. Its Imported by count of 2 is a weak adoption signal; it is the default TOML package of the rotini CLI framework.

Unverified leads: `github.com/pelletier/go-toml` v1.9.5 (3,687 Imported by) loads the service-config control but fails typed-scalars with `incorrect date/time separation character` because its lexer accepts only EOF, a space or `T` after a local date. `github.com/naoina/toml` v0.1.1 (2,071) implements TOML 0.4 and rejects `octal = 0o755` with `line 7: invalid TOML syntax`; its 2018 fork `github.com/influxdata/toml` (136) fails the same line and cannot decode service-config into a map. `github.com/creachadair/tomledit/parser` v0.0.29 (46) returns values only as raw token text. `github.com/midbel/toml` v1.0.5 (24) returns all four date-time kinds as `time.Time` and decodes `\u00e9` as `I`. `github.com/komkom/toml` v0.1.2 (18) streams the document as JSON with date-times as strings. `github.com/lixenwraith/toml` v0.10.0 (5) rejects date-times and underscored integers. `github.com/kezhuw/toml` (3, TOML 0.4.0) was not run. Forks of BurntSushi/toml (`hydronica/toml`, `chef/toml`, `troian/toml`, `GuanceCloud/toml`) are excluded with their shared-line counts. Evidence is in [leads.json](leads.json).
