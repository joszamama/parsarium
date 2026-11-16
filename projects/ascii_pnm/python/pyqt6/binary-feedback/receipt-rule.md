# Proposed native binary feedback receipt

This is a proposal for the shared audit. Existing project manifests remain staged until the audit implements and verifies it.

```json
{
  "coverage_kind": "native_binary_edges",
  "module": {"path": "/absolute/path/libParser.so", "sha256": "64 hex digits", "role": "documented format parser library"},
  "instrumentation": {"engine": "afl++-qemu", "release": "5.04a", "image_digest": "sha256:..."},
  "control": {"path": "controls/...", "sha256": "64 hex digits", "observed": {"format_aware_result": true}},
  "mapping": {"module_text_range": "0x...-0x...", "executable_excluded_range": "0x...-0x..."},
  "feedback": {"control_tuples": 754, "repeat_map_equal": true, "variant_tuples": 747, "variant_map_differs": true, "module_excluded_tuples": 1},
  "source_lines_covered": null,
  "decoder_function_attribution": false
}
```

The audit may accept `native_binary_edges` only when all of these conditions hold:

1. The pinned package and tool image reproduce, and the selected module's SHA-256 matches the receipt. The module path belongs to that package; documentation identifies it as containing the format parser or its runtime library.
2. The ordinary project control produces the expected format-aware result. The binary driver accepts a local file, bytes, or a stream and produces an observable result for the same valid control.
3. QEMU's mapped executable range for the selected module is recorded and disjoint from the excluded host executable range. The coverage run selects only the module's executable range and excludes the host executable. A probe discovers the mapping; no unchecked fixed address is trusted.
4. The same control yields the same nontrivial map twice. A second valid format control yields a different map. Excluding the selected module reduces feedback to a small residual baseline, here at most two tuples. Each run exits successfully without timeout.
5. The receipt explicitly sets `source_lines_covered` to `null` and does not claim decoder-function attribution unless symbol or address evidence separately establishes it. Counts from this mode are reported as binary tuples, separate from source lines and Python wrapper tuples.

Acceptance supports a **library-level native binary feedback** label. It does not by itself prove coverage of a specific decoder function inside a large shared library such as Qt GUI. Any stronger claim needs a separately instrumented source build or symbol-level address evidence.
