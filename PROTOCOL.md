# Parser selection protocol (v3, 2026-11-13)

Eligibility rules were written before the pilot. Version 2 records the user's
20-per-cell working goal; it does not change eligibility. The unit of analysis is one
ecosystem × format cell. The ten formats and eight ecosystems are listed in
`data/cells.json`.

Version 3 clarifies selection after the user pointed out that verified parsing
alone does not establish popularity. For each cell, inspect plausible candidates
with stronger adoption evidence before adding obscure or unranked candidates.
The working goal is subject to this selection rule. A count of 20 does not
establish that the included set is the 20 most used packages when the search
surface is bounded or adoption metrics are missing.

## Eligibility and verification

An included parser must be an open-source, version-pinned library or a documented
standard/runtime API that accepts local bytes, a local file, or a local stream
and interprets the target format. It must expose at least one observable
format-specific result (for example dimensions, entries, tags, or fields) from
a small valid control. Merely opening a file, copying bytes, identifying a
filename or MIME type, searching for signatures, or handing input to a remote
service does not qualify. Wrappers qualify when their local API parses the
format, but the underlying parser family is recorded. A package appears once
per cell even when it exposes several APIs.

For each accepted release, record its exact version, license evidence,
documentation for the input API, a control file, a runnable adapter, expected
structured output, and a successful run with environment and date. The adapter
must read the supplied control path; a hard-coded output is invalid. A candidate
remains a *lead* until all of these checks pass. Unsupported or unavailable
dependencies and ambiguous APIs remain unresolved leads, never accepted rows.

Controls are minimal valid examples of the named variant: ASCII for PLY and
PNM, HTTP/1.1 for HTTP, and MP3 with ID3v2 for the MP3 cell. Coverage beyond the
control's feature subset is not implied by one successful run. No malformed
input or performance experiments are in scope.

## Discovery, stopping, and counts

For each cell, search its ecosystem registry using the format name and common
parser/decoder/reader terms, then inspect the highest-ranked relevant results
and project documentation. Save the exact queries, date, result limit, and
lead dispositions. Search hits are discovery material, not parser evidence.
Inspect at most the first 100 results per query and aim for 20 distinct
*verified* third-party packages per cell. Twenty is the working goal following
the 2026-11-11 user revision; the original ceiling of 30 remains. Twenty is
never a quota to fill with unrelated software. A batch may stop at the working
goal after the listed query windows are saved and plausible higher-download
leads have been checked or explicitly marked unresolved. Before the goal,
stop only after the listed searches and relevant documentation leads have been
reviewed, or when a stated environmental limit prevents further checks. Every summary gives the actual
verified count, searched surface, number of leads still unresolved, and a
plain-language account of what could have been missed.

## Popularity

Rank only verified third-party packages within the same ecosystem and cell.
Use one documented metric, source, and observation window per ranking. Prefer
registry download counts over GitHub stars; when the registry lacks comparable
counts, use one consistently collected ecosystem-specific metric and name its
limits. Do not extrapolate absent values, combine unlike metrics, compare
scores across ecosystems, or rank standard-library/runtime APIs against
packages. An unavailable metric is `null` and leaves its order unresolved.
Popularity is an adoption proxy, not a quality or security judgment.
Additional adoption signals can be recorded separately, with their source and
date, but must not be mixed into the primary ranking or used to infer a missing
primary value. Label packages without a comparable primary metric as unranked,
and state when this prevents a defensible top-N claim.

## Standard libraries and runtime bundles

Inspect official API documentation independently for every cell. A documented
candidate still requires the same control and observable output to become
verified. Record an explicit `none_documented` finding only when the searched
official documentation and its scope are stated. Otherwise use `pending` or
`unresolved`; silence is not evidence of absence. Bundled APIs are kept outside
third-party rankings, including wrappers over system libraries.

## Reproducibility and uncertainty

Registry search hits and metric responses are dated snapshots. Repository
data separates leads, verified parsers, standard APIs, and cell summaries.
Record versions and transitive lockfiles where available. Commands must run
from a fresh checkout using the README instructions. A failed or unrun check
must stay visible with its reason. Shared parser families prevent misleading
independence claims. Revisit conclusions when sources or versions change;
do not silently replace pinned evidence.
