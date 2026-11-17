# github.com/bytedance/sonic — JSON / Go

**Pilot / incomplete format cell.** This path is verified on two valid controls; the format-wide search remains bounded and incomplete.

- **Pinned release:** `v1.15.5`
- **License:** Apache-2.0
- **Parser family:** Sonic optimized arm64 decoder, Go `optdec` over native NEON parser
- **Local input API:** `sonic.Unmarshal([]byte, *any)`
- **API reference:** [Go Packages](https://pkg.go.dev/github.com/bytedance/sonic@v1.15.5#Unmarshal)
- **Valid controls:** [nested object](../../../../controls/json/nested-object.json) and [nested array](../../../../controls/json/nested-array.json)
- **Evidence:** [parser record](../../../../data/go/json/parsers.json), [control result](../../../../data/go/json/verification.json), [AFL++ feedback](../../../../fuzzing/afl-native/json/go/github_com_bytedance_sonic/differential.json)

The harness checks `sonic.APIKind == sonic.UseSonicJSON` before parsing, so the pinned build cannot silently use the `encoding/json` fallback. Go source instrumentation covers 289 lines in Sonic `internal/decoder/optdec` on the object control. Repeated parser-only AFL++ traces are identical for the same control and differ by 35 parser features and 35 AFL++ tuples for the valid nested array. NEON assembly instructions are outside Go source coverage.

The saved pkg.go.dev snapshot reports 2,428 importing packages for Sonic. This is a package adoption count, not evidence that every importer calls JSON decoding.

## Run

```sh
python3 parsarium.py build json go github_com_bytedance_sonic
python3 parsarium.py run json go github_com_bytedance_sonic controls/json/nested-object.json
python3 parsarium.py run json go github_com_bytedance_sonic controls/json/nested-array.json
```
