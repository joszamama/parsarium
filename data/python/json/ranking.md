# Python × JSON: pilot ranking

Two third-party paths are control verified so far; nine targeted documentation leads were recorded, and seven remain unverified. The ten-path ceiling is not a quota. The bounded PyPI Simple Index search is pending, so this is not a claim about the definitive most-used JSON parsers.

The comparable within-cell signal is [PyPI Stats](https://pypistats.org/api/) `last_month` package downloads excluding known mirrors, observed 2026-11-17 around 02:24 UTC. It measures adoption of entire packages, including transitive installs and uses unrelated to JSON parsing. Unverified leads with higher download counts are recorded in [leads.json](leads.json) but are not ranked as verified parsers.

| Rank among verified | Package | Release | Last-month downloads | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [pydantic](https://docs.pydantic.dev/latest/api/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_json) | 2.14.3 | 1,139,429,690 | JSON structure and values from local bytes via `TypeAdapter[Any].validate_json` | pydantic-core 2.50.4 / Jiter 0.18.0 |
| 2 | [simplejson](https://simplejson.readthedocs.io/en/latest/) | 4.3.0 | 49,365,386 | JSON structure and values from a local binary stream | simplejson pure-Python decoder |

The standalone `jiter` package has 421,162,504 last-month downloads in the lead log. It shares Pydantic's Jiter parser family but is not a verified package path here. Both selected paths have pinned container controls, parser-scoped coverage, and AFL++ feedback; the [Pydantic native receipt](pydantic-valid-feedback.json) checks repeated, input-dependent Jiter source regions on two valid controls. The [CPython `json` standard API](standard.json) is recorded separately, without a third-party popularity rank.

The Pydantic LLVM export warned about mismatched profile data in 99 whole-extension functions. Its coverage claim is limited to the scoped Jiter regions recorded in the verification receipt; complete extension coverage is not established.
