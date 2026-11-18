# Parser selection protocol

Parsarium evaluates one **format × ecosystem cell** at a time. Ten selected third-party package paths is a ceiling, not a quota. Standard/runtime APIs are inventoried separately and do not use that ceiling. A package path may share an underlying parser with another package; shared families are recorded.

## Eligibility

A parser must be an open-source, pinned library release or a documented standard/runtime API that accepts a local file, byte buffer, stream, or in-memory text and interprets the named format. Text input qualifies for textual formats such as JSON and XML when the adapter obtains it locally and the package API itself parses its structure. Verification requires a small valid control and an observable format-specific result, such as dimensions, entries, pages, tags, samples, or protocol fields. Generic file I/O, filename or MIME detection, byte copying, signature search, and remote services do not qualify. A wrapper can qualify as a package API, with its underlying parser family identified.

An empty compatibility distribution that only installs another selected parser package is not a separate parser path, even if importing the installed dependency succeeds.

A concrete-syntax-tree grammar, such as a tree-sitter grammar on the tree-sitter runtime, qualifies only if the harness can produce the cell's observable result by reading node kinds and node text from the tree. The harness may do what accepted adapters already do: read token text, strip literal delimiters, and type scalar tokens from their literal text. The grammar does not qualify if the harness would have to supply format semantics that the library leaves out, such as decoding string escapes or entity and character references, folding or chomping block scalars, resolving aliases, merging dotted keys and table headers into one tree, or resolving namespaces beyond the raw-name precedent. Such a grammar stays a lead under the tokenizer precedent of C JSON jsmn.

Each accepted path records its release and license evidence, documented input API, control, expected output, adapter, observed result, and environment. A registry hit or project name remains a *lead* until these checks pass. The valid control establishes only the tested format subset.

## Discovery and stopping

Registry searches use the format name and relevant parser, decoder, or reader terms. Each query, date, result limit, hit count, and unresolved lead is recorded. Search hits stay separate from verified parsers. Search inspection is bounded to the first 100 results per query, followed by project documentation and plausible high-adoption leads.

A cell reports its actual selected count, search surface, unresolved leads, and what remains uncertain. A count below ten is acceptable when the bounded search or available adoption evidence does not support more choices. Ten paths do not establish a definitive most-used ten.

After the adoption ranking, a selected third-party path also needs a pinned container control and parser-derived AFL++ feedback to remain in the runnable collection. A path that cannot meet that gate is excluded with its control and blocker evidence recorded; the slot is left open rather than filled with an unverified lower-ranked lead. The slot may be refilled only by the next path in primary-rank order that has itself passed the container control and parser-derived AFL++ feedback gate; an unverified next-ranked path stops the refill. This runnability gate does not change its recorded adoption metric or deny that the package parses the tested control.

## Popularity

Third-party packages are ranked only among verified paths in the **same cell**. One documented primary metric, source, and observation window is used per ranking. Registry downloads are preferred when comparable; an ecosystem-specific alternative is named when needed. Missing values remain `null` or unranked. Metrics are not invented, mixed into one rank, or compared across ecosystems. Standard and runtime APIs remain outside third-party rankings. Popularity is an adoption proxy, not a quality or security judgment.

The ten-path curation first keeps positive primary-metric paths in descending order. A primary-unranked C/C++ path may use a separately labeled Debian Popcon source-package installation count of at least 1,000; where a multi-library source package makes that count format-ambiguous, a format-specific binary development-package installation count of at least 1,000 may serve as the fallback instead. At most three such paths per non-PLY cell receive slots. PLY cells, and C and C++ cells of every format, may fill slots that remain empty after the primary-metric and Debian-fallback paths with pinned tagged releases of upstream GitHub repositories with at least 100 stars (`stargazers_count`, captured with a timestamp in the cell's snapshot). A star-fallback path never displaces a primary or Debian path. The repository must be the parser library itself and not a fork or mirror: a framework, engine or multi-purpose library whose stars reflect other features does not qualify, by the same rule that keeps GLib's GMarkup unranked. These signals are separately ranked and never treated as numerically comparable to the primary metric. An identical short package name does not establish Debian source identity. A path with zero or missing evidence is not added just to reach ten. One byte-identical PHP PLY parser-family duplicate is excluded. The saved [selection plan](data/curation/plan.json) records every retained and removed path, metric, source snapshot hash, and reason. The thresholds are curation rules, not claims that a particular number proves use of the format.

## Standard APIs and reproducibility

Official documentation is searched separately for standard-library and runtime-bundled APIs in every cell. A documented API needs the same control and observable result for verification. `none_documented`, `pending`, and `unresolved` describe distinct outcomes; silence is not evidence of absence.

Registry snapshots, source locks, parser evidence, controls, and receipts remain in `data/`, `adapters/`, `controls/`, and `projects/`. Unselected paths with incomplete parser feedback remain in the curation decision record. Every selected third-party path has a verified container harness and AFL++ overlay; standard/runtime APIs are reported separately, including honest staged controls when native instrumentation is unavailable. Fuzzing launcher checks do not establish vulnerability findings.
