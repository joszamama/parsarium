# Parser selection protocol

Parsarium evaluates one **format × ecosystem cell** at a time. The working goal is 20 verified third-party package paths per cell, with 30 as a ceiling. A count is never filled with unrelated software. A package path may share an underlying parser with another package; shared families are recorded.

## Eligibility

A parser must be an open-source, pinned library release or a documented standard/runtime API that accepts local bytes, a local file, or a local stream and interprets the named format. Verification requires a small valid control and an observable format-specific result, such as dimensions, entries, pages, tags, samples, or protocol fields. Generic file I/O, filename or MIME detection, byte copying, signature search, and remote services do not qualify. A wrapper can qualify as a package API, with its underlying parser family identified.

Each accepted path records its release and license evidence, documented input API, control, expected output, adapter, observed result, and environment. A registry hit or project name remains a *lead* until these checks pass. The valid control establishes only the tested format subset.

## Discovery and stopping

Registry searches use the format name and relevant parser, decoder, or reader terms. Each query, date, result limit, hit count, and unresolved lead is recorded. Search hits stay separate from verified parsers. Search inspection is bounded to the first 100 results per query, followed by project documentation and plausible high-adoption leads.

A cell may stop at the 20-path working goal when the saved query windows and plausible stronger-adoption leads have been inspected or marked unresolved. Below 20, stopping requires a recorded search limit or environmental blocker. Every cell reports the actual verified count, search surface, unresolved leads, and what remains uncertain. Twenty verified paths do not automatically establish the definitive most-used 20.

## Popularity

Third-party packages are ranked only among verified paths in the **same cell**. One documented metric, source, and observation window is used per ranking. Registry downloads are preferred when comparable; an ecosystem-specific alternative is named when needed. Missing values remain `null` or unranked. Metrics are not invented, mixed, or compared across ecosystems. Standard and runtime APIs remain outside third-party rankings. Popularity is an adoption proxy, not a quality or security judgment.

## Standard APIs and reproducibility

Official documentation is searched separately for standard-library and runtime-bundled APIs in every cell. A documented API needs the same control and observable result for verification. `none_documented`, `pending`, and `unresolved` describe distinct outcomes; silence is not evidence of absence.

Registry snapshots, source locks, parser evidence, controls, and receipts remain in `data/`, `adapters/`, `controls/`, and `projects/`. Failed or unrun checks stay visible with their reasons. Container harnesses are a verified runnable subset of the catalog. Fuzzing launcher checks are recorded separately from parser selection and do not establish vulnerability findings.
