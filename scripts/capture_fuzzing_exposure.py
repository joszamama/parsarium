#!/usr/bin/env python3
"""Record whether each selected third-party parser path is already fuzzed upstream.

Writes data/curation/fuzzing-exposure.json: one row per parser path in
data/<ecosystem>/<format>/parsers.json, keyed "<eco>/<fmt>/<name>" like
data/curation/upstream-repositories.json, whose `repository` field is the only
source of upstream URLs used here. Nothing is guessed: a path without a
repository, or whose repository is not on github.com, gets `not_checked` with
the reason for every signal that needs the repository host.

Signals
-------

oss_fuzz
    A pinned snapshot of google/oss-fuzz (sparse checkout of
    projects/*/project.yaml at one commit, recorded in the output). A path is
    integrated when a project's `main_repo`, normalized the same way as
    upstream repositories (scheme, `git@host:` form, `.git` suffix, trailing
    path parts and case removed), equals the path's normalized repository URL.
    This check needs only the URL, so it runs for any non-null repository,
    GitHub or not. Projects whose name equals the package name or the
    repository name, but whose `main_repo` differs, are recorded in
    `name_only_projects` as a secondary signal and do not set the value.
    `disabled: true` in the project.yaml is recorded.

in_repo_harness (HEURISTIC)
    For GitHub repositories only: one GraphQL query per batch of repositories
    reads each default branch and its head commit; one REST tree listing
    (GET /repos/{owner}/{repo}/git/trees/{commit}?recursive=1) per repository
    is then matched against file and directory naming conventions. A libFuzzer
    entry point (LLVMFuzzerTestOneInput) cannot be seen in a tree, so the rules
    are name rules, applied case-insensitively to paths outside vendored
    directories (any path component in VENDORED):

      fuzz_directory       a path component named fuzz, fuzzing, fuzzers or oss-fuzz
      fuzz_file            a file named *fuzz*.{c,cc,cpp,rs,go,py,js,ts,java,php}
                           ("fuzzy" does not count; Go *_test.go files are
                           handled by the two Go rules instead)
      cargo_fuzz           a fuzz/Cargo.toml (cargo-fuzz layout)
      go_native_fuzz_test  a *fuzz*_test.go whose content declares
                           func FuzzXxx(f *testing.F); at most 3 such files are
                           fetched per repository
      go_fuzz_unknown      *fuzz*_test.go files exist but the fetched ones (at
                           most 3) do not confirm a native fuzz test and more
                           remain unfetched
      jazzer_build_file    pom.xml / build.gradle(.kts) mentioning jazzer; at
                           most 2 build files (shortest paths first) are fetched,
                           only for repositories of Java paths
      atheris_dependency   requirements*.txt / pyproject.toml / setup.py /
                           setup.cfg mentioning atheris, or a file named
                           *atheris*; at most 2 files fetched, only for
                           repositories of Python paths

    Content probes (the Go, Jazzer and Atheris fetches) run only when no tree
    rule has matched, so a repository costs one tree request plus at most five
    content requests. Up to 5 matching paths are recorded per rule. value is
    true when a rule other than go_fuzz_unknown matched, null when only
    go_fuzz_unknown matched or when the tree listing was truncated without a
    match, and false otherwise.

    Known blind spots: fuzz targets that do not follow the naming conventions
    (e.g. Go fuzz tests in plain *_test.go files, harnesses under tests/ named
    after the API), harnesses kept in a separate repository or only in
    OSS-Fuzz's own projects/<name>/ directory, fuzzing on non-default branches,
    property-based tests that happen to be called "fuzz", and vendored copies
    inside directories not listed in VENDORED. Rules are repository-wide; for a
    monorepo row with `directory`, `in_directory` tells whether any matched
    path lies under that directory.

adoption rank
    The row's rank and metric value in its cell's ranking.md, read with the
    website's ranking parser (website/build.py ranking_rows plus the same
    name-matching fallbacks). rank is null when the ranking table does not list
    the path; the analysis can then join on the cell.

Every GitHub response is cached under --cache (raw bytes plus capture time) so
reruns are cheap; rows record captured_at_utc and the sha256 of each raw
response they rely on. Only read calls are made (`gh api` GET and GraphQL
queries). No fuzzer is run.

Usage:
  python3 scripts/capture_fuzzing_exposure.py --oss-fuzz DIR --cache DIR [--workers N]

DIR for --oss-fuzz is a checkout of google/oss-fuzz with projects/*/project.yaml,
for example:
  git clone --depth 1 --filter=blob:none --no-checkout https://github.com/google/oss-fuzz.git DIR
  git -C DIR sparse-checkout set --no-cone '/projects/*/project.yaml' && git -C DIR checkout
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha1, sha256
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/curation/fuzzing-exposure.json"
UPSTREAM = ROOT / "data/curation/upstream-repositories.json"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "website"))

from capture_upstream_repositories import normalize_repo  # noqa: E402

ECOSYSTEMS = ("c", "cpp", "go", "java", "javascript", "php", "python", "rust")
FUZZ_DIRS = {"fuzz", "fuzzing", "fuzzers", "oss-fuzz"}
FUZZ_EXTS = {"c", "cc", "cpp", "rs", "go", "py", "js", "ts", "java", "php"}
VENDORED = {"third_party", "third-party", "thirdparty", "3rdparty", "vendor", "vendored",
            "node_modules", "external", "extern", "deps"}
FUZZ_WORD = re.compile(r"fuzz(?!y)", re.I)
GO_FUZZ_FUNC = re.compile(rb"func\s+Fuzz\w*\s*\(\s*\w+\s+\*testing\.F\s*\)")
JAVA_BUILD = {"pom.xml", "build.gradle", "build.gradle.kts"}
PY_DEPS = re.compile(r"^(requirements[^/]*\.txt|pyproject\.toml|setup\.py|setup\.cfg)$", re.I)
MAX_PATHS = 5
MAX_GO_FETCH = 3
MAX_BUILD_FETCH = 2
GRAPHQL_BATCH = 40
RULES = ("fuzz_directory", "fuzz_file", "cargo_fuzz", "go_native_fuzz_test", "go_fuzz_unknown",
         "jazzer_build_file", "atheris_dependency")
HEURISTIC = ("in_repo_harness is a file-name heuristic over one default-branch tree listing, "
             "with at most five bounded content probes; it is not proof that a harness runs.")


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


# --------------------------------------------------------------------------- GitHub (read only)

class GitHub:
    def __init__(self, cache: Path):
        self.cache = cache
        cache.mkdir(parents=True, exist_ok=True)
        self.requests = 0

    def _get(self, key: str, argv: list[str]):
        stem = self.cache / sha1(key.encode()).hexdigest()
        body, meta = stem.with_suffix(".body"), stem.with_suffix(".meta.json")
        if body.exists() and meta.exists():
            m = json.loads(meta.read_text())
            return body.read_bytes(), m
        proc = subprocess.run(["gh", "api", *argv], capture_output=True)
        self.requests += 1
        m = {"request": key, "captured_at_utc": now(), "exit_code": proc.returncode,
             "stderr": proc.stderr.decode(errors="replace")[-500:]}
        # Do not cache transient failures (rate limits, 5xx); 404/409/422 are kept.
        if proc.returncode != 0 and not re.search(r"HTTP (404|409|422)|Could not resolve", m["stderr"]) \
                and not proc.stdout.strip().startswith(b"{"):
            return proc.stdout, m
        body.write_bytes(proc.stdout)
        meta.write_text(json.dumps(m))
        return proc.stdout, m

    def rest(self, path: str, raw: bool = False):
        argv = ["-H", "Accept: application/vnd.github.raw"] if raw else []
        return self._get(("RAW " if raw else "GET ") + path, [*argv, path])

    def graphql(self, query: str):
        return self._get("GRAPHQL " + query, ["graphql", "-f", f"query={query}"])


def owner_repo(url: str):
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)$", url)
    return (m.group(1), m.group(2)) if m else None


def heads(gh: GitHub, repos: list[str]) -> dict:
    """Default branch and head commit per GitHub repository URL."""
    out = {}
    for start in range(0, len(repos), GRAPHQL_BATCH):
        batch = repos[start:start + GRAPHQL_BATCH]
        parts = []
        for i, url in enumerate(batch):
            owner, name = owner_repo(url)
            parts.append(f'r{i}: repository(owner: {json.dumps(owner)}, name: {json.dumps(name)}) '
                         '{ nameWithOwner isArchived defaultBranchRef { name target { oid } } }')
        query = "query { " + " ".join(parts) + " }"
        body, meta = gh.graphql(query)
        digest = sha256(body).hexdigest()
        try:
            data = (json.loads(body) or {}).get("data") or {}
        except json.JSONDecodeError:
            data = {}
        for i, url in enumerate(batch):
            node = data.get(f"r{i}")
            ref = (node or {}).get("defaultBranchRef")
            out[url] = {
                "name_with_owner": node and node["nameWithOwner"],
                "archived": node and node["isArchived"],
                "default_branch": ref and ref["name"],
                "commit": ref and ref["target"]["oid"],
                "captured_at_utc": meta["captured_at_utc"],
                "response_sha256": digest,
            }
    return out


# --------------------------------------------------------------------------- harness rules

def vendored(path: str) -> bool:
    return any(part.casefold() in VENDORED for part in path.split("/")[:-1])


def tree_rules(paths: list[str]) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {}
    seen_dirs = set()
    for path in paths:
        if vendored(path):
            continue
        parts = path.split("/")
        low = path.casefold()
        for depth, part in enumerate(parts[:-1]):
            if part.casefold() in FUZZ_DIRS:
                d = "/".join(parts[:depth + 1])
                if d not in seen_dirs:
                    seen_dirs.add(d)
                    hits.setdefault("fuzz_directory", []).append(d)
                break
        base = parts[-1]
        stem, _, ext = base.rpartition(".")
        if low == "fuzz/cargo.toml" or low.endswith("/fuzz/cargo.toml"):
            hits.setdefault("cargo_fuzz", []).append(path)
        if stem and ext.casefold() in FUZZ_EXTS and FUZZ_WORD.search(stem) \
                and not base.casefold().endswith("_test.go"):
            hits.setdefault("fuzz_file", []).append(path)
    return hits


def detect(gh: GitHub, url: str, head: dict, ecosystems: set[str]) -> dict:
    owner, name = owner_repo(url)
    result = {"status": "checked", "heuristic": True, "value": None, "rules": [],
              "default_branch": head["default_branch"], "repository_commit": head["commit"],
              "head_query_sha256": head["response_sha256"], "tree_truncated": False,
              "content_probes": []}
    if head.get("archived"):
        result["archived"] = True
    api = f"repos/{owner}/{name}/git/trees/{head['commit']}?recursive=1"
    body, meta = gh.rest(api)
    result.update(evidence_url=f"https://api.github.com/{api}",
                  browse_url=f"https://github.com/{owner}/{name}/tree/{head['commit']}",
                  captured_at_utc=meta["captured_at_utc"], response_sha256=sha256(body).hexdigest())
    try:
        tree = json.loads(body)
        entries = tree["tree"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return {"status": "not_checked", "value": None,
                "reason": f"tree listing failed (gh exit {meta['exit_code']})",
                "evidence_url": result["evidence_url"], "captured_at_utc": meta["captured_at_utc"],
                "response_sha256": result["response_sha256"]}
    result["tree_truncated"] = bool(tree.get("truncated"))
    files = [e["path"] for e in entries if e.get("type") == "blob"]
    result["tree_files"] = len(files)
    hits = tree_rules(files)

    def fetch(path: str) -> bytes:
        body, meta = gh.rest(f"repos/{owner}/{name}/contents/{path}?ref={head['commit']}", raw=True)
        result["content_probes"].append({"path": path, "captured_at_utc": meta["captured_at_utc"],
                                         "response_sha256": sha256(body).hexdigest(),
                                         "ok": meta["exit_code"] == 0})
        return body if meta["exit_code"] == 0 else b""

    if not hits:
        unvendored = [p for p in files if not vendored(p)]
        go_tests = sorted((p for p in unvendored if p.casefold().endswith("_test.go")
                           and FUZZ_WORD.search(p.rsplit("/", 1)[-1])), key=lambda p: (p.count("/"), p))
        if go_tests:
            confirmed = [p for p in go_tests[:MAX_GO_FETCH] if GO_FUZZ_FUNC.search(fetch(p))]
            if confirmed:
                hits["go_native_fuzz_test"] = confirmed
            elif len(go_tests) > MAX_GO_FETCH:
                hits["go_fuzz_unknown"] = go_tests[MAX_GO_FETCH:]
        if "java" in ecosystems and not hits:
            builds = sorted((p for p in unvendored if p.rsplit("/", 1)[-1] in JAVA_BUILD),
                            key=lambda p: (p.count("/"), p))[:MAX_BUILD_FETCH]
            found = [p for p in builds if b"jazzer" in fetch(p).lower()]
            if found:
                hits["jazzer_build_file"] = found
        if "python" in ecosystems and not hits:
            named = [p for p in unvendored if "atheris" in p.rsplit("/", 1)[-1].casefold()]
            if named:
                hits["atheris_dependency"] = named
            else:
                deps = sorted((p for p in unvendored if PY_DEPS.match(p.rsplit("/", 1)[-1])),
                              key=lambda p: (p.count("/"), p))[:MAX_BUILD_FETCH]
                found = [p for p in deps if b"atheris" in fetch(p).lower()]
                if found:
                    hits["atheris_dependency"] = found
    result["rules"] = [{"rule": rule, "matches": len(hits[rule]), "paths": hits[rule][:MAX_PATHS]}
                       for rule in RULES if rule in hits]
    if any(rule != "go_fuzz_unknown" for rule in hits):
        result["value"] = True
    elif hits or result["tree_truncated"]:
        result["value"] = None
        result["reason"] = ("only go_fuzz_unknown matched" if hits
                            else "tree listing truncated by the API and no rule matched")
    else:
        result["value"] = False
    if not result["content_probes"]:
        del result["content_probes"]
    return result


# --------------------------------------------------------------------------- OSS-Fuzz

def repo_key(url: str | None) -> str | None:
    if not url:
        return None
    url = url.strip().strip("'\"")
    norm = normalize_repo(url)
    if norm:
        return norm.casefold().rstrip("/")
    url = re.sub(r"^(git\+)?(https?|git|svn|ssh)://", "", url, flags=re.I)
    url = re.sub(r"^git@([^:]+):", r"\1/", url)
    url = re.sub(r"^www\.", "", url, flags=re.I)
    url = re.sub(r"\.git/?$", "", url.rstrip("/"))
    return "https://" + url.casefold().rstrip("/")


def load_oss_fuzz(root: Path) -> tuple[str, str, dict]:
    sha = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True,
                         text=True, check=True).stdout.strip()
    date = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%cI"], capture_output=True,
                          text=True, check=True).stdout.strip()
    projects = {}
    for path in sorted((root / "projects").glob("*/project.yaml")):
        raw = path.read_bytes()
        text = raw.decode(errors="replace")
        m = re.search(r"^main_repo:\s*(\S+)", text, re.M)
        projects[path.parent.name] = {
            "main_repo": m.group(1).strip("'\"") if m else None,
            "key": repo_key(m.group(1)) if m else None,
            "disabled": bool(re.search(r"^disabled:\s*true\s*$", text, re.M | re.I)),
            "sha256": sha256(raw).hexdigest(),
        }
    return sha, date, projects


def oss_fuzz_row(entry: dict, repo: str | None, sha: str, projects: dict, by_key: dict) -> dict:
    if not repo:
        return {"status": "not_checked", "value": None,
                "reason": "null_repository",
                "note": "no upstream repository recorded in upstream-repositories.json"}

    def describe(name):
        p = projects[name]
        out = {"project": name, "main_repo": p["main_repo"],
               "evidence_url": f"https://github.com/google/oss-fuzz/blob/{sha}/projects/{name}/project.yaml",
               "project_yaml_sha256": p["sha256"]}
        if p["disabled"]:
            out["disabled"] = True
        return out

    matched = by_key.get(repo_key(repo), [])
    repo_name = repo.rstrip("/").rsplit("/", 1)[-1].removesuffix(".git").casefold()
    candidates = {entry["name"].casefold().rsplit("/", 1)[-1], repo_name}
    name_only = sorted(n for n in projects if n.casefold() in candidates and n not in matched)
    row = {"status": "checked", "value": bool(matched), "match": "main_repo_url" if matched else None,
           "projects": [describe(n) for n in matched]}
    if name_only:
        row["name_only_projects"] = [describe(n) for n in name_only]
    return row


# --------------------------------------------------------------------------- ranks

def load_ranks():
    import build as site  # website/build.py; guarded by __main__

    cells = {}
    for collection, path in (("active", ROOT / "data/cells.json"), ("pilot", ROOT / "data/pilot-cells.json")):
        for cell in json.loads(path.read_text())["cells"]:
            cells[(cell["ecosystem"], cell["format"])] = collection

    def ranks_for(eco, fmt, entries):
        path = ROOT / f"data/{eco}/{fmt}/ranking.md"
        if not path.exists():
            return {}
        ranks = site.ranking_rows(path, eco)
        normalized, by_release = {}, {}
        for n, row in ranks.items():
            normalized.setdefault(re.sub(r"[^a-z0-9]", "", n), []).append(row)
            by_release.setdefault(row[2], []).append(row)
        release_counts = {}
        for e in entries:
            release_counts[e["version"]] = release_counts.get(e["version"], 0) + 1
        out = {}
        for entry in entries:
            n = entry["name"]
            hit = ranks.get(n.casefold())
            alias = site.RANKING_ALIASES.get((eco, fmt, n))
            if not hit and alias and alias.casefold() in ranks:
                hit = ranks[alias.casefold()]
            if not hit:
                norm = normalized.get(re.sub(r"[^a-z0-9]", "", n.casefold()), [])
                if len(norm) == 1:
                    hit = norm[0]
            if not hit:
                suffix = [r for k, r in ranks.items() if "/" in k and n.casefold().endswith("/" + k)
                          and r[2] == entry["version"]]
                if len(suffix) == 1:
                    hit = suffix[0]
            if not hit:
                same = by_release.get(entry["version"], [])
                if release_counts[entry["version"]] == 1 and len(same) == 1:
                    hit = same[0]
            out[n] = hit
        return out

    return cells, ranks_for


# --------------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--oss-fuzz", type=Path, required=True)
    ap.add_argument("--cache", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    upstream = json.loads(UPSTREAM.read_text())["rows"]
    sha, sha_date, projects = load_oss_fuzz(args.oss_fuzz)
    by_key: dict[str, list[str]] = {}
    for n, p in projects.items():
        if p["key"]:
            by_key.setdefault(p["key"], []).append(n)
    cells, ranks_for = load_ranks()

    entries = []
    for eco in ECOSYSTEMS:
        for path in sorted((ROOT / "data" / eco).glob("*/parsers.json")):
            fmt = path.parent.name
            rows = json.loads(path.read_text())
            ranks = ranks_for(eco, fmt, rows)
            for row in rows:
                entries.append((eco, fmt, row, ranks.get(row["name"])))

    github = {}
    for eco, fmt, row, _ in entries:
        repo = upstream[f"{eco}/{fmt}/{row['name']}"]["repository"]
        if repo and owner_repo(repo):
            github.setdefault(repo, set()).add(eco)
    gh = GitHub(args.cache)
    head = heads(gh, sorted(github))

    def run(url):
        h = head[url]
        if not h["commit"]:
            return url, {"status": "not_checked", "value": None,
                         "reason": "GitHub GraphQL returned no default branch (repository missing, "
                                   "renamed without redirect, or empty)",
                         "head_query_sha256": h["response_sha256"], "captured_at_utc": h["captured_at_utc"]}
        return url, detect(gh, url, h, github[url])

    with ThreadPoolExecutor(args.workers) as pool:
        harness = dict(pool.map(run, sorted(github)))

    out_rows = {}
    for eco, fmt, row, rank in entries:
        key = f"{eco}/{fmt}/{row['name']}"
        up = upstream[key]
        repo = up["repository"]
        record = {"ecosystem": eco, "format": fmt, "name": row["name"], "version": row["version"],
                  "collection": cells.get((eco, fmt)), "repository": repo}
        if up.get("directory"):
            record["repository_directory"] = up["directory"]
        record["adoption"] = ({"rank": rank[0], "metric_value": rank[1], "metric": rank[3],
                               "source": f"data/{eco}/{fmt}/ranking.md"} if rank else
                              {"rank": None, "source": f"data/{eco}/{fmt}/ranking.md",
                               "note": "ranking table does not list this path; join on the cell"})
        record["oss_fuzz"] = oss_fuzz_row(row, repo, sha, projects, by_key)
        if not repo:
            record["in_repo_harness"] = {"status": "not_checked", "value": None, "reason": "null_repository",
                                         "note": up.get("repository_note")}
        elif not owner_repo(repo):
            host = repo.split("/")[2]
            record["in_repo_harness"] = {"status": "not_checked", "value": None, "reason": "non_github_host",
                                         "host": host}
        else:
            h = dict(harness[repo])
            if up.get("directory") and h.get("rules"):
                prefix = up["directory"].rstrip("/") + "/"
                h["in_directory"] = any(p.startswith(prefix) or p + "/" == prefix
                                        for r in h["rules"] for p in r["paths"])
            record["in_repo_harness"] = h
        out_rows[key] = record

    summary = summarize(out_rows)
    doc = {
        "schema_version": 1,
        "description": ("Fuzzing exposure of every selected third-party parser path: OSS-Fuzz integration "
                        "(pinned google/oss-fuzz snapshot) and in-repository fuzz harnesses (heuristic). "
                        "Written by scripts/capture_fuzzing_exposure.py."),
        "heuristic_label": HEURISTIC,
        "captured_at_utc": now(),
        "oss_fuzz_snapshot": {"repository": "https://github.com/google/oss-fuzz", "commit": sha,
                              "committed_at": sha_date, "projects": len(projects),
                              "projects_with_main_repo": sum(1 for p in projects.values() if p["key"])},
        "in_repo_harness_rules": list(RULES),
        "vendored_directories_ignored": sorted(VENDORED),
        "summary": summary,
        "rows": out_rows,
    }
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps(summary, indent=1))
    print(f"GitHub requests made this run: {gh.requests}", file=sys.stderr)
    return 0


def summarize(rows: dict) -> dict:
    def count(it):
        out = {}
        for k in it:
            out[k] = out.get(k, 0) + 1
        return dict(sorted(out.items()))

    s = {"rows": len(rows),
         "oss_fuzz": count(("true" if r["oss_fuzz"]["value"] else "false") if r["oss_fuzz"]["status"] == "checked"
                           else "not_checked:" + r["oss_fuzz"]["reason"] for r in rows.values()),
         "oss_fuzz_name_only": sum(1 for r in rows.values() if r["oss_fuzz"].get("name_only_projects")),
         "in_repo_harness": count(("not_checked:" + r["in_repo_harness"]["reason"])
                                  if r["in_repo_harness"]["status"] == "not_checked"
                                  else {True: "true", False: "false", None: "unknown"}[r["in_repo_harness"]["value"]]
                                  for r in rows.values()),
         "in_repo_harness_by_rule": count(rule["rule"] for r in rows.values()
                                          for rule in r["in_repo_harness"].get("rules", [])),
         "either_true": sum(1 for r in rows.values() if r["oss_fuzz"]["value"] or r["in_repo_harness"]["value"]),
         "by_ecosystem": {}}
    for eco in ECOSYSTEMS:
        sub = [r for r in rows.values() if r["ecosystem"] == eco]
        s["by_ecosystem"][eco] = {
            "rows": len(sub),
            "harness_checked": sum(1 for r in sub if r["in_repo_harness"]["status"] == "checked"),
            "oss_fuzz_true": sum(1 for r in sub if r["oss_fuzz"]["value"]),
            "in_repo_harness_true": sum(1 for r in sub if r["in_repo_harness"]["value"]),
            "either_true": sum(1 for r in sub if r["oss_fuzz"]["value"] or r["in_repo_harness"]["value"]),
        }
    return s


if __name__ == "__main__":
    sys.exit(main())
