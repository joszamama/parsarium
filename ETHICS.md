# Ethics and responsible use

Parsarium collects more than a thousand open-source parsers and makes each one easy to run, measure, and fuzz. Many of these packages are small, maintained by one or two volunteers, and have probably never been fuzzed. Putting them side by side in a ready-to-use testbed has real benefits for research and for the packages themselves, and it also shifts work and risk onto their maintainers. This document says what Parsarium does, what it does not do, and what we ask of people who use it.

## What Parsarium is

- **A research testbed.** Its purpose is to make parser experiments reproducible and comparable: pinned releases, documented input APIs, valid controls, coverage, and fuzzing harnesses.
- **Built only from public material.** Every target is a published release of open-source software, fetched from its public registry or repository and pinned by version and hash. Parsarium does not include private, leaked, or proprietary code.
- **Built with valid inputs only.** Each target was verified with small, well-formed control files. While building the catalog we did not run malformed-input campaigns, vulnerability searches, or resource-exhaustion experiments against the targets, and the repository ships no crashing inputs, exploits, or proof-of-concept files.

## What inclusion means

- Inclusion is **not a security assessment**. A package being in the catalog says nothing about whether it is safe or unsafe.
- Rankings use public adoption signals (downloads, dependents, installations, stars) **within one format and language**. They describe how widely a package is used, not its quality, and they are not an endorsement.
- Each package keeps its own license, recorded in the catalog. Parsarium's harnesses and data are Apache-2.0; that license does not cover the third-party code they run.

## What we ask of users

If you fuzz Parsarium targets, you are likely to find bugs. Please treat them as you would treat bugs you found in any other project:

1. **Run locally.** Use the provided containers on your own machines. Do not point Parsarium harnesses, generated inputs, or corpora at services, websites, or infrastructure you do not own or are not authorized to test.
2. **Triage before reporting.** Reproduce the crash outside the fuzzer, reduce it, deduplicate it by failure location and parser family, and check the latest upstream release. Many packages share an engine; one bug in a shared library should become one report to that library, not dozens of reports to its wrappers. The [triage and disclosure chapter](https://parsarium.com/manual/triage-and-disclosure/) of the manual walks through these steps.
3. **Disclose privately first.** Use the channel named in the project's security policy (`SECURITY.md`, GitHub private vulnerability reporting, or a distribution security team). Do not open public issues, pull requests, or posts containing crashing inputs for unfixed security bugs. Give maintainers reasonable time to respond and fix; ninety days is a common default.
4. **Be considerate of maintainers.** Do not mass-file automated reports. Send reduced inputs, the exact release, a reproduction command, and your assessment of impact. Offer a fix when you can.
5. **Publish responsibly.** When you write about results, report aggregate findings, credit the maintainers, and do not publish reproducers for issues that are still unfixed.

## Maintainers

If you maintain a package in Parsarium and want it described differently, linked to a security policy, or removed from the catalog, open an issue on the [GitHub repository](https://github.com/joszamama/parsarium/issues). We will act on such requests promptly.
