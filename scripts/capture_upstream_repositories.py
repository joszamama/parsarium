#!/usr/bin/env python3
"""Link every selected third-party parser path to its upstream repository.

Writes data/curation/upstream-repositories.json: one row per parser path in
data/<ecosystem>/<format>/parsers.json, keyed "<eco>/<fmt>/<name>", with

  repository     canonical browsable source repository (https), or null
  directory      subdirectory inside a monorepo, when the registry names one
  registry_url   package page (PyPI, npm, crates.io, Packagist, pkg.go.dev,
                 Maven Central, Conan Center or the Debian tracker), or null
  source         how the repository was established
  evidence_url   the recorded or fetched URL that established it
  verification   the HTTP check of the repository URL

Facts already in the repository come first: the parser record's own source
fields, the cell and project source locks, the cell registry snapshot and the
GitHub supplemental star capture. Registry metadata is fetched only to fill
gaps (PyPI project_urls, npm repository, crates.io repository, Packagist
source, Maven POM scm, Go go-import/go-source meta, Debian upstream metadata).
Fetched rows carry captured_at_utc and response_sha256. Nothing is guessed: a
row with no established repository has repository null and a repository_note.

Rows whose name, version and evidence are unchanged are carried over from the
previous file; pass --refresh to fetch everything again.

Usage: python3 scripts/capture_upstream_repositories.py [--refresh] [--offline]
(macOS python.org builds need SSL_CERT_FILE=/etc/ssl/cert.pem. Set PARSARIUM_HTTP_CACHE to a
directory to keep raw responses between runs.)
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/curation/upstream-repositories.json"
STARS = ROOT / "data/curation/github-supplemental-stars.json"
PLAN = ROOT / "data/curation/plan.json"
UA = "parsarium-research (upstream repository links)"
ECOSYSTEMS = ("c", "cpp", "go", "java", "javascript", "php", "python", "rust")

# Repositories that host recipes or ports for many packages; never a parser's upstream.
AGGREGATORS = {
    "github.com/conan-io/conan-center-index", "github.com/microsoft/vcpkg",
    "github.com/homebrew/homebrew-core", "github.com/definitelytyped/definitelytyped",
    "github.com/msys2/mingw-packages", "github.com/nixos/nixpkgs",
}
GITHUB_RESERVED = {"orgs", "sponsors", "apps", "marketplace", "features", "topics",
                   "search", "settings", "login", "about", "collections", "users"}
GITLAB_HOSTS = re.compile(r"^(gitlab\.[a-z0-9.-]+|salsa\.debian\.org|framagit\.org|invent\.kde\.org|"
                          r"code\.videolan\.org|git\.ffmpeg\.org)$")
# Fields of a parser record that name the package's own source.
SOURCE_FIELDS = ("source", "source_url", "source_lock", "repository", "packagist_source_reference")
# Fields that may point into the package's repository but also elsewhere.
DOC_FIELDS = ("documentation", "license_evidence", "documentation_evidence", "documentation_site",
              "api_documentation", "supporting_documentation", "documentation_archive_entry")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# --------------------------------------------------------------------------- URLs

def normalize_repo(url: str | None) -> str | None:
    """Return a canonical https repository URL, or None if url is not one."""
    if not url or not isinstance(url, str):
        return None
    u = url.strip()
    u = re.sub(r"^git\+", "", u)
    m = re.match(r"^(?:ssh://)?git@([^:/]+)[:/](.+)$", u)
    if m:
        u = f"https://{m.group(1)}/{m.group(2)}"
    u = re.sub(r"^(git|http|svn)://", "https://", u)
    if not u.startswith("https://"):
        if re.match(r"^github:[\w.-]+/[\w.-]+$", u):
            u = "https://github.com/" + u.split(":", 1)[1]
        else:
            return None
    parts = urllib.parse.urlsplit(u)
    host = parts.netloc.lower().split("@")[-1].split(":")[0]
    if host == "www.github.com":
        host = "github.com"
    segs = [s for s in parts.path.split("/") if s]
    if host in ("github.com", "codeload.github.com", "raw.githubusercontent.com", "api.github.com"):
        if host == "api.github.com":
            if len(segs) < 3 or segs[0] != "repos":
                return None
            segs = segs[1:]
        if len(segs) < 2 or segs[0].lower() in GITHUB_RESERVED:
            return None
        owner, repo = segs[0], re.sub(r"\.git$", "", segs[1])
        if not repo:
            return None
        out = f"https://github.com/{owner}/{repo}"
    elif host in ("bitbucket.org", "codeberg.org", "gitea.com", "git.sr.ht"):
        if len(segs) < 2:
            return None
        out = f"https://{host}/{segs[0]}/{re.sub(r'.git$', '', segs[1])}"
    elif GITLAB_HOSTS.match(host) or host == "gitlab.com":
        path = parts.path.split("/-/")[0]
        segs = [s for s in path.split("/") if s]
        cut = next((i for i, s in enumerate(segs) if s in ("tree", "blob", "raw", "archive", "tags",
                                                            "releases", "uploads", "commit", "issues")), None)
        if cut is not None:
            segs = segs[:cut]
        if len(segs) < 2:
            return None
        segs[-1] = re.sub(r"\.git$", "", segs[-1])
        out = f"https://{host}/" + "/".join(segs)
    elif host == "sourceforge.net":
        if len(segs) >= 2 and segs[0] in ("projects", "p"):
            out = f"https://sourceforge.net/projects/{segs[1]}/"
        else:
            return None
    elif host in ("launchpad.net", "code.launchpad.net"):
        if not segs or segs[0][0] in "~+":
            return None
        out = f"https://launchpad.net/{segs[0]}"
    elif host == "code.qt.io":
        m = re.match(r"^/cgit/(.+?\.git)", parts.path)
        if not m:
            return None
        out = f"https://code.qt.io/cgit/{m.group(1)}/"
    elif host == "gitbox.apache.org":
        m = re.search(r"(?:^|[;&])p=([\w.-]+?)(?:\.git)?(?:[;&]|$)", parts.query) or \
            re.match(r"^/repos/asf/([\w.-]+?)(?:\.git)?/?$", parts.path)
        if not m:
            return None
        out = f"https://gitbox.apache.org/repos/asf?p={m.group(1)}.git"
    elif host.endswith(".googlesource.com"):
        if not segs:
            return None
        cut = next((i for i, s in enumerate(segs) if s.startswith("+")), len(segs))
        out = f"https://{host}/" + "/".join(segs[:cut])
    else:
        return None
    if out.lower() in {"https://" + a for a in AGGREGATORS}:
        return None
    if host == "salsa.debian.org":
        return None  # Debian packaging repositories, not upstream
    return out


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)


def first_repo(values) -> tuple[str, str] | None:
    for v in values:
        for s in strings(v):
            for m in re.finditer(r"(?:git\+)?(?:https?|git|ssh)://[^\s\"'<>)]+|git@[^\s\"'<>)]+", s):
                repo = normalize_repo(m.group(0).rstrip(".,;"))
                if repo:
                    return repo, m.group(0).rstrip(".,;")
    return None


def norm_token(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def name_matches_repo(name: str, repo: str) -> bool:
    """True when the repository's own name plausibly is this package (docs-derived fallback only)."""
    tail = norm_token(repo.rstrip("/").split("/")[-1])
    pieces = [norm_token(p) for p in re.split(r"[/:]", name) if p]
    pieces = [p for p in pieces if len(p) >= 3]
    return any(p in tail or tail in p for p in pieces if tail)


# --------------------------------------------------------------------------- HTTP

class Fetcher:
    def __init__(self, offline: bool):
        self.offline = offline
        self.lock = threading.Lock()
        self.cache: dict[str, tuple[int, bytes, str]] = {}
        cache_dir = os.environ.get("PARSARIUM_HTTP_CACHE")
        self.cache_dir = Path(cache_dir) if cache_dir else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.token = os.environ.get("GITHUB_TOKEN")
        if not self.token and not offline:
            try:
                self.token = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True,
                                            timeout=20).stdout.strip() or None
            except (OSError, subprocess.SubprocessError):
                self.token = None

    def get(self, url: str, accept: str | None = None) -> tuple[int, bytes, str]:
        """Return (status, body, final_url); status 0 means a network failure."""
        if self.offline:
            raise RuntimeError("offline")
        with self.lock:
            if url in self.cache:
                return self.cache[url]
        disk = None
        if self.cache_dir:
            disk = self.cache_dir / sha256(url.encode()).hexdigest()
            if disk.exists():
                meta = json.loads(disk.with_suffix(".json").read_text())
                result = (meta["status"], disk.read_bytes(), meta["final"])
                with self.lock:
                    self.cache[url] = result
                return result
        headers = {"User-Agent": UA}
        if accept:
            headers["Accept"] = accept
        if self.token and url.startswith("https://api.github.com/"):
            headers["Authorization"] = f"Bearer {self.token}"
        result = (0, b"", url)
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=60) as r:
                    result = (r.status, r.read(), r.geturl())
                break
            except urllib.error.HTTPError as e:
                if e.code in (429, 502, 503, 504) and attempt < 3:
                    time.sleep(4 * (attempt + 1))
                    continue
                result = (e.code, e.read() if e.fp else b"", url)
                break
            except ValueError:
                break
            except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
                if attempt < 3:
                    time.sleep(3 * (attempt + 1))
                    continue
        with self.lock:
            self.cache[url] = result
        if disk and result[0] in (200, 404, 410):
            disk.write_bytes(result[1])
            disk.with_suffix(".json").write_text(json.dumps({"url": url, "status": result[0], "final": result[2]}))
        return result

    def json(self, url: str):
        status, body, _ = self.get(url, "application/json")
        if status != 200:
            return None, status, body
        return json.loads(body), status, body


# --------------------------------------------------------------------------- identities

def load(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def maven_coordinate(row: dict) -> tuple[str, str] | None:
    if row.get("group") and row.get("artifact"):
        return row["group"], row["artifact"]
    coord = row.get("coordinate")
    if isinstance(coord, str) and coord.count(":") >= 1:
        g, a = coord.split(":")[:2]
        return g, a
    for s in strings(row):
        m = re.search(r"/maven2/(.+?)/([^/]+)/([^/]+)/\2-\3[^/]*\.(?:jar|pom)", s)
        if m:
            return m.group(1).replace("/", "."), m.group(2)
        m = re.search(r"javadoc\.io/(?:static|doc)/([^/]+)/([^/]+)/", s)
        if m:
            return m.group(1), m.group(2)
        m = re.search(r"maven/packages/([^/:%]+)(?::|%3A)([^/?]+)", s)
        if m:
            return m.group(1), m.group(2)
        m = re.search(rf"\b([a-z][\w.-]*\.[\w.-]+):{re.escape(row['name'])}:", s)
        if m:
            return m.group(1), row["name"]
    return None


def debian_source(row: dict, plan_entry: dict | None) -> str | None:
    pop = row.get("popularity") or row.get("metric") or {}
    if isinstance(pop, dict):
        for key in ("source_package", "debian_source", "debian_source_package"):
            if isinstance(pop.get(key), str):
                return pop[key]
        m = re.search(r"source package ([a-z0-9][a-z0-9+.-]+)", str(pop.get("metric") or pop.get("name") or ""))
        if m:
            return m.group(1)
        for s in strings(pop):
            m = re.search(r"sources\.debian\.org/src/([a-z0-9][a-z0-9+.-]+)", s) or \
                re.search(r"tracker\.debian\.org/pkg/([a-z0-9][a-z0-9+.-]+)", s)
            if m:
                return m.group(1)
    for s in strings({k: v for k, v in row.items() if k in ("documentation", "license_evidence", "source")}):
        m = re.search(r"sources\.debian\.org/src/([a-z0-9][a-z0-9+.-]+)", s)
        if m:
            return m.group(1)
    if plan_entry:
        for s in strings(plan_entry):
            m = re.search(r"sources\.debian\.org/src/([a-z0-9][a-z0-9+.-]+)", s)
            if m:
                return m.group(1)
    return None


def registry_identity(eco: str, row: dict, lock_entry: dict | None, deb: str | None):
    """Return (kind, key, registry_url) for the package page."""
    name = row["name"]
    q = urllib.parse.quote
    if eco == "python":
        if not re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]*$", name):
            # display name for one loader of a package; take the PyPI name the record cites
            m = next((re.search(r"pypi\.org/(?:pypi|project)/([A-Za-z0-9._-]+)", s) for s in strings(row)
                      if re.search(r"pypi\.org/(?:pypi|project)/([A-Za-z0-9._-]+)", s)), None)
            if not m:
                return None, None, None
            name = m.group(1)
        return "pypi", name, f"https://pypi.org/project/{name}/"
    if eco == "javascript":
        return "npm", name, f"https://www.npmjs.com/package/{name}"
    if eco == "rust":
        return "crates", name, f"https://crates.io/crates/{name}"
    if eco == "php":
        if "/" in name:
            return "packagist", name, f"https://packagist.org/packages/{name}"
        return None, None, None
    if eco == "go":
        return "go", (row.get("module"), name), f"https://pkg.go.dev/{name}"
    if eco == "java":
        coord = maven_coordinate(row)
        if coord:
            g, a = coord
            return "maven", coord, f"https://central.sonatype.com/artifact/{q(g)}/{q(a)}"
        return None, None, None
    # C and C++: Conan Center when the source lock names it, else the Debian tracker.
    for s in strings(lock_entry or {}):
        if "conan.io/center/recipes/" in s:
            return "conan", s, s.rstrip("/")
    if deb:
        return "debian", deb, f"https://tracker.debian.org/pkg/{deb}"
    return None, None, None


# --------------------------------------------------------------------------- registry metadata

def fetched(url: str, body: bytes) -> dict:
    return {"evidence_url": url, "captured_at_utc": now(), "response_sha256": sha256(body).hexdigest()}


def from_pypi(f: Fetcher, name: str, version: str):
    url = f"https://pypi.org/pypi/{name}/{version}/json"
    data, status, body = f.json(url)
    if data is None:
        url = f"https://pypi.org/pypi/{name}/json"
        data, status, body = f.json(url)
    if data is None:
        return None, f"PyPI JSON returned HTTP {status}"
    info = data.get("info") or {}
    urls = info.get("project_urls") or {}
    order = sorted(urls.items(), key=lambda kv: next(
        (i for i, k in enumerate(("source", "repository", "code", "github", "gitlab", "homepage", "home"))
         if k in kv[0].lower()), 99))
    for label, value in order:
        repo = normalize_repo(value)
        if repo:
            return {"repository": repo, "source": f"PyPI JSON info.project_urls[{label!r}]",
                    **fetched(url, body)}, None
    repo = normalize_repo(info.get("home_page"))
    if repo:
        return {"repository": repo, "source": "PyPI JSON info.home_page", **fetched(url, body)}, None
    home = next((v for v in urls.values() if isinstance(v, str) and v.startswith("http")), info.get("home_page"))
    return None, {"note": "PyPI metadata names no source repository", "homepage": home, **fetched(url, body)}


def from_npm(f: Fetcher, name: str, version: str):
    enc = name.replace("/", "%2F")
    url = f"https://registry.npmjs.org/{enc}/{version}"
    data, status, body = f.json(url)
    if data is None:
        return None, f"npm registry returned HTTP {status}"
    repo_field = data.get("repository")
    directory = None
    raw = None
    if isinstance(repo_field, dict):
        raw, directory = repo_field.get("url"), repo_field.get("directory")
    elif isinstance(repo_field, str):
        raw = repo_field
        if re.match(r"^[\w.-]+/[\w.-]+$", raw):
            raw = "https://github.com/" + raw
    repo = normalize_repo(raw)
    if repo:
        out = {"repository": repo, "source": "npm registry version metadata repository", **fetched(url, body)}
        if directory:
            out["directory"] = directory.strip("/")
        return out, None
    for field in ("homepage",):
        repo = normalize_repo(data.get(field))
        if repo:
            return {"repository": repo, "source": f"npm registry version metadata {field}",
                    **fetched(url, body)}, None
    bugs = data.get("bugs")
    repo = normalize_repo(bugs.get("url") if isinstance(bugs, dict) else bugs)
    if repo:
        return {"repository": repo, "source": "npm registry version metadata bugs.url",
                **fetched(url, body)}, None
    return None, {"note": "npm metadata names no source repository", "homepage": data.get("homepage"),
                  **fetched(url, body)}


def from_crates(f: Fetcher, name: str, version: str):
    url = f"https://crates.io/api/v1/crates/{name}"
    data, status, body = f.json(url)
    if data is None:
        return None, f"crates.io API returned HTTP {status}"
    crate = data.get("crate") or {}
    for field in ("repository", "homepage"):
        repo = normalize_repo(crate.get(field))
        if repo:
            return {"repository": repo, "source": f"crates.io API crate.{field}", **fetched(url, body)}, None
    return None, {"note": "crates.io metadata names no source repository",
                  "homepage": crate.get("homepage") or crate.get("documentation"), **fetched(url, body)}


def from_packagist(f: Fetcher, name: str, version: str):
    url = f"https://repo.packagist.org/p2/{name}.json"
    data, status, body = f.json(url)
    if data is None:
        return None, f"Packagist returned HTTP {status}"
    versions = (data.get("packages") or {}).get(name) or []
    pick = next((v for v in versions if v.get("version") in (version, "v" + version)), versions[0] if versions else {})
    for label, value in (("source.url", (pick.get("source") or {}).get("url")),
                         ("support.source", (pick.get("support") or {}).get("source")),
                         ("homepage", pick.get("homepage"))):
        repo = normalize_repo(value)
        if repo:
            return {"repository": repo, "source": f"Packagist metadata {label}", **fetched(url, body)}, None
    return None, {"note": "Packagist metadata names no source repository", "homepage": pick.get("homepage"),
                  **fetched(url, body)}


def pom_text(root: ET.Element, path: str) -> str | None:
    ns = {"m": "http://maven.apache.org/POM/4.0.0"}
    el = root.find("/".join("m:" + p for p in path.split("/")), ns)
    if el is None:
        el = root.find(path)
    return el.text.strip() if el is not None and el.text else None


def from_maven(f: Fetcher, coord: tuple[str, str], version: str):
    """The release POM's own scm/url; else deps.dev SOURCE_REPO (resolved from the effective POM).

    A parent POM's scm describes the parent project (Maven appends the child's
    artifactId on inheritance), so it is never taken as is.
    """
    g, a = coord
    url = f"https://repo.maven.apache.org/maven2/{g.replace('.', '/')}/{a}/{version}/{a}-{version}.pom"
    status, body, _ = f.get(url)
    homepage = None
    if status == 200:
        try:
            root = ET.fromstring(body)
        except ET.ParseError:
            root = None
        if root is not None:
            for path in ("scm/url", "scm/connection", "scm/developerConnection", "url"):
                value = pom_text(root, path)
                if value and "${" not in value:
                    repo = normalize_repo(re.sub(r"^scm:(git|svn|hg):", "", value))
                    if repo:
                        return {"repository": repo, "source": "Maven POM " + path.replace("/", "."),
                                **fetched(url, body)}, None
            homepage = pom_text(root, "url")
    q = urllib.parse.quote
    dd = f"https://api.deps.dev/v3/systems/maven/packages/{q(g + ':' + a, safe='')}/versions/{q(version)}"
    data, dstatus, dbody = f.json(dd)
    if data:
        links = data.get("links") or []
        for link in links:
            if link.get("label") == "SOURCE_REPO":
                repo = normalize_repo(re.sub(r"^scm:(git|svn|hg):", "", link.get("url") or ""))
                if repo:
                    return {"repository": repo, "source": "deps.dev Maven version links SOURCE_REPO (effective POM)",
                            **fetched(dd, dbody)}, None
        homepage = homepage or next((l.get("url") for l in links if l.get("label") == "HOMEPAGE"), None)
        return None, {"note": "Maven POM and deps.dev name no reachable source repository", "homepage": homepage,
                      **fetched(dd, dbody)}
    if status != 200:
        return None, f"Maven Central POM returned HTTP {status}"
    return None, {"note": "Maven POM names no source repository", "homepage": homepage, **fetched(url, body)}


def go_meta(f: Fetcher, path: str):
    url = f"https://{path}?go-get=1"
    status, body, _ = f.get(url)
    if status != 200:
        return None, None, url, body
    text = body.decode("utf-8", "replace")
    imp = src = None
    for m in re.finditer(r"<meta\s+[^>]*name=[\"']go-(import|source)[\"'][^>]*>", text, re.I):
        content = re.search(r"content=[\"']([^\"']+)[\"']", m.group(0))
        if not content:
            continue
        fields = html.unescape(content.group(1)).split()
        if m.group(1).lower() == "import" and len(fields) >= 3 and path.startswith(fields[0]):
            if imp is None or len(fields[0]) > len(imp[0]):
                imp = fields
        elif m.group(1).lower() == "source" and len(fields) >= 2 and path.startswith(fields[0]):
            src = fields
    return imp, src, url, body


def from_go(f: Fetcher, ident, version: str):
    module, name = ident
    path = module or name
    repo = normalize_repo("https://" + path)
    if repo and path.split("/")[0] in ("github.com", "gitlab.com", "bitbucket.org", "codeberg.org"):
        return {"repository": repo, "source": "Go module path on its code host", "evidence_url": None}, None
    imp, src, url, body = go_meta(f, path)
    if imp:
        repo = normalize_repo(imp[2])
        if repo:
            return {"repository": repo, "source": "Go go-import meta (repo root)", **fetched(url, body)}, None
        if src and len(src) >= 2:
            repo = normalize_repo(src[1])
            if repo:
                return {"repository": repo, "source": "Go go-source meta (home)", **fetched(url, body)}, None
        if imp[2].startswith("https://") and not imp[2].startswith("https://gopkg.in/"):
            # the module's declared VCS root on a host normalize_repo does not know
            root = re.sub(r"\.git$", "", imp[2].rstrip("/"))
            return {"repository": root, "source": "Go go-import meta (repo root)", **fetched(url, body)}, None
        if imp[2].startswith("https://gopkg.in/"):
            # gopkg.in documents its mapping: gopkg.in/pkg.vN -> github.com/go-pkg/pkg,
            # gopkg.in/user/pkg.vN -> github.com/user/pkg.
            segs = imp[2].split("/")[3:]
            base = re.sub(r"\.v\d+$", "", segs[-1])
            owner = segs[0] if len(segs) == 2 else "go-" + base
            return {"repository": f"https://github.com/{owner}/{base}",
                    "source": "gopkg.in documented path mapping", **fetched(url, body)}, None
    return None, f"no go-import meta at {url}" if body is None else {
        "note": "Go import path resolves to no code-host repository", "homepage": f"https://{path}",
        **(fetched(url, body) if body else {})}


def release_major(version: str) -> str | None:
    """Leading numeric component of a release, without a Debian epoch or revision."""
    m = re.match(r"^(?:\d+:)?v?(\d+)[.\-+~]", str(version) + ".")
    return m.group(1) if m else None


def debian_area_version(f: Fetcher, pkg: str, release: str | None = None):
    """Area and version of a Debian source package (sid first).

    With a release, only versions whose upstream major number equals the
    release's count, so a same-named package for another major line (Debian
    sqlite is SQLite 2) is not taken for this one.
    """
    data, status, body = f.json(f"https://sources.debian.org/api/src/{pkg}/")
    if not data or data.get("error") or not data.get("versions"):
        return None
    versions = data["versions"]
    if release is not None:
        major = release_major(release)
        versions = [v for v in versions if major and release_major(v["version"]) == major]
        if not versions:
            return None
    pick = next((v for v in versions if "sid" in (v.get("suites") or [])), versions[0])
    return pick.get("area", "main"), pick["version"]


def from_debian(f: Fetcher, pkg: str, release: str | None = None):
    found = debian_area_version(f, pkg, release)
    if not found:
        return None, (f"Debian sources has no source package {pkg}" if release is None else
                      f"Debian sources has no source package {pkg} for release line {release}")
    area, version = found
    prefix = pkg[:4] if pkg.startswith("lib") else pkg[0]
    base = f"https://sources.debian.org/data/{area}/{prefix}/{pkg}/{version}/debian"
    url = base + "/upstream/metadata"
    status, body, _ = f.get(url)
    if status == 200:
        text = body.decode("utf-8", "replace")
        for key in ("Repository-Browse", "Repository"):
            m = re.search(rf"^{key}:\s*(\S+)", text, re.M)
            repo = normalize_repo(m.group(1)) if m else None
            if repo:
                return {"repository": repo, "source": f"Debian {pkg} {version} debian/upstream/metadata {key}",
                        **fetched(url, body)}, None
    url = base + "/control"
    status, body, _ = f.get(url)
    if status == 200:
        text = body.decode("utf-8", "replace")
        m = re.search(r"^Homepage:\s*(\S+)", text, re.M)
        repo = normalize_repo(m.group(1)) if m else None
        if repo:
            return {"repository": repo, "source": f"Debian {pkg} {version} debian/control Homepage",
                    **fetched(url, body)}, None
        return None, {"note": f"Debian {pkg} records no upstream repository (no debian/upstream/metadata "
                              f"Repository; Homepage is not a code host)",
                      "homepage": m.group(1) if m else None, **fetched(url, body)}
    return None, f"Debian {pkg} control unavailable"


# --------------------------------------------------------------------------- verification

def verify(f: Fetcher, repo: str) -> dict:
    checked = now()
    if repo.startswith("https://github.com/"):
        owner_repo = repo.split("github.com/")[1]
        status, body, _ = f.get(f"https://api.github.com/repos/{owner_repo}", "application/vnd.github+json")
        if status == 200:
            data = json.loads(body)
            out = {"method": "GitHub REST repos API", "status": 200, "checked_at_utc": checked,
                   "canonical": data["html_url"]}
            if data.get("archived"):
                out["archived"] = True
            if data.get("fork") and data.get("parent"):
                out["fork_of"] = data["parent"]["html_url"]
            return out
        return {"method": "GitHub REST repos API", "status": status, "checked_at_utc": checked}
    status, _, final = f.get(repo)
    out = {"method": "HTTPS GET", "status": status, "checked_at_utc": checked}
    if final.rstrip("/") != repo.rstrip("/"):
        out["final_url"] = final
    return out


# --------------------------------------------------------------------------- main

def rows_by_cell():
    for eco in ECOSYSTEMS:
        for path in sorted((ROOT / "data" / eco).glob("*/parsers.json")):
            fmt = path.parent.name
            for row in json.loads(path.read_text()):
                yield eco, fmt, row


def snapshot_repo(snapshot, name: str):
    """Code-host URL recorded for this package anywhere in a cell registry snapshot."""
    hits = []

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == name and isinstance(v, dict):
                    hits.append(v)
                walk(v)
            if node.get("name") == name or node.get("package") == name or node.get("candidate") == name:
                hits.append({k: v for k, v in node.items() if k in ("repository", "repository_url", "url",
                                                                     "source_url", "html_url", "homepage")})
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(snapshot)
    for hit in hits:
        # owner/name plus a GitHub API URL
        for key in ("url", "source_url", "repository_url", "html_url", "repository", "homepage"):
            repo = normalize_repo(hit.get(key)) if isinstance(hit.get(key), str) else None
            if repo:
                return repo, hit[key]
    return None


def recorded(eco, fmt, row, cell_lock, cell_snapshot, stars, plan_entry):
    name = row["name"]
    found = first_repo([row.get(k) for k in SOURCE_FIELDS])
    if found:
        return {"repository": found[0], "source": "parser record source URL", "evidence_url": found[1]}
    lock_entry = (cell_lock or {}).get(name)
    if isinstance(lock_entry, dict):
        top = {k: v for k, v in lock_entry.items() if isinstance(v, str)}
        if re.match(r"^[\w.-]+/[\w.-]+$", top.get("repository", "")) and "github" in json.dumps(lock_entry):
            top["repository"] = "https://github.com/" + top["repository"]
        found = first_repo([top.get(k) for k in ("repository", "source_url", "source", "tag", "url")])
        if found:
            return {"repository": found[0], "source": "cell source lock", "evidence_url": found[1]}
    project = row.get("project")
    if project:
        pdir = ROOT / project
        if pdir.suffix:
            pdir = pdir.parent
        plock = load(pdir / "source-lock.json")
        if isinstance(plock, dict):
            entry = plock.get(name) or (next(iter(plock.values())) if len(plock) == 1 else None)
            if isinstance(entry, dict):
                top = {k: v for k, v in entry.items() if isinstance(v, str)}
                found = first_repo([top.get(k) for k in ("repository", "source_url", "source", "tag", "url")])
                if found:
                    return {"repository": found[0], "source": "project source lock", "evidence_url": found[1]}
            top = {k: v for k, v in plock.items() if isinstance(v, str)}
            found = first_repo([top.get(k) for k in ("repository", "source_url", "source", "tag", "url")])
            if found:
                return {"repository": found[0], "source": "project source lock", "evidence_url": found[1]}
    star = stars.get(f"{eco}/{name}")
    if star:
        repo = normalize_repo(star.get("resolved_url") or star.get("source_url"))
        if repo:
            return {"repository": repo, "source": "GitHub supplemental star capture",
                    "evidence_url": star.get("source_url")}
    pop = row.get("popularity") or row.get("metric")
    if isinstance(pop, dict) and "github" in str(pop.get("metric") or pop.get("name") or "").lower():
        found = first_repo([pop.get("source"), pop.get("url")])
        if found:
            return {"repository": found[0], "source": "parser record GitHub star metric", "evidence_url": found[1]}
    if cell_snapshot:
        found = snapshot_repo(cell_snapshot, name)
        if found:
            return {"repository": found[0], "source": "cell registry snapshot", "evidence_url": found[1]}
    return None


def documented(row):
    found = first_repo([row.get(k) for k in DOC_FIELDS])
    if found and name_matches_repo(row["name"], found[0]):
        return {"repository": found[0], "source": "parser record documentation URL on the code host",
                "evidence_url": found[1]}
    return None


def candidates(f: Fetcher, eco, fmt, row, ctx, kind, key, deb):
    """Yield (hit, miss) in priority order; hit is a dict with repository, miss a note."""
    cell_lock, cell_snapshot, stars, plan_entry = ctx
    hit = recorded(eco, fmt, row, cell_lock, cell_snapshot, stars, plan_entry)
    if hit:
        yield hit, None
    if f.offline:
        yield documented(row), None
        return
    fetchers = {"pypi": from_pypi, "npm": from_npm, "crates": from_crates, "packagist": from_packagist,
                "maven": from_maven, "go": from_go, "debian": from_debian}
    if kind in fetchers:
        # a recorded Debian source package is taken as recorded, whatever its release line
        yield fetchers[kind](f, key, None if kind == "debian" else str(row["version"]))
    if eco in ("c", "cpp") and kind != "debian" and deb:
        yield from_debian(f, deb)
    yield documented(row), None
    if eco in ("c", "cpp") and not deb and re.match(r"^[a-z0-9][a-z0-9+.-]+$", row["name"]):
        hit, miss = from_debian(f, row["name"], str(row["version"]))
        if hit:
            hit["source"] = hit["source"].replace("Debian ", "Debian source package of the same name ", 1)
        yield hit, miss


def resolve(f: Fetcher, eco, fmt, row, ctx) -> dict:
    name, version = row["name"], str(row["version"])
    cell_lock, cell_snapshot, stars, plan_entry = ctx
    lock_entry = (cell_lock or {}).get(name) if isinstance(cell_lock, dict) else None
    deb = debian_source(row, plan_entry) if eco in ("c", "cpp") else None
    kind, key, registry_url = registry_identity(eco, row, lock_entry, deb)
    if registry_url is None and eco in ("c", "cpp") and not f.offline \
            and re.match(r"^[a-z0-9][a-z0-9+.-]+$", name) and debian_area_version(f, name, version):
        registry_url = f"https://tracker.debian.org/pkg/{name}"
        out_registry_source = "Debian source package of the same name"
    else:
        out_registry_source = None
    out = {"ecosystem": eco, "format": fmt, "name": name, "version": version,
           "repository": None, "registry_url": registry_url}
    if out_registry_source:
        out["registry_source"] = out_registry_source
    miss = None
    rejected = []
    for hit, why in candidates(f, eco, fmt, row, ctx, kind, key, deb):
        if why and not (isinstance(miss, dict) and isinstance(why, str)):
            miss = miss if isinstance(miss, dict) else why
        if not hit or any(r["repository"] == hit["repository"] for r in rejected):
            continue
        if not f.offline:
            check = verify(f, hit["repository"])
            if check["status"] in (404, 410):
                rejected.append({"repository": hit["repository"], "source": hit["source"],
                                 "status": check["status"]})
                continue
            canonical = check.get("canonical")
            if canonical and canonical.lower() != hit["repository"].lower():
                check["requested"] = hit["repository"]
                hit["repository"] = canonical
            elif canonical and canonical != hit["repository"]:
                hit["repository"] = canonical
            check.pop("canonical", None)
            if check["status"] == 0:
                check["note"] = "host did not resolve or answer from the capture host; not verified"
            hit["verification"] = check
        out.update(hit)
        break
    if rejected:
        out["rejected"] = rejected
    if not out.get("repository"):
        out["source"] = None
        note = miss if isinstance(miss, dict) else {"note": miss}
        text = note.get("note") or "No source repository is recorded for this package"
        if rejected:
            text = "; ".join(f"{r['source']} names {r['repository']}, which returns HTTP {r['status']}"
                             for r in rejected) + ". " + text
        out["repository_note"] = text
        for k in ("homepage", "evidence_url", "captured_at_utc", "response_sha256"):
            if note.get(k):
                out[k] = note[k]
        if not out.get("homepage"):
            doc = row.get("documentation")
            if isinstance(doc, str) and doc.startswith("https://"):
                out["homepage"] = doc
        if out.get("homepage") and not str(out["homepage"]).startswith("https://"):
            out["homepage_http"] = out.pop("homepage")
    return out


def propagate(rows: dict) -> None:
    """Fill a null row from the same package established in another cell (C and C++ share packages)."""
    group = {"c": "c", "cpp": "c"}
    known = {}
    for key, row in rows.items():
        if row.get("repository") and row.get("source") and not row["source"].startswith("same package"):
            known.setdefault((group.get(row["ecosystem"], row["ecosystem"]), row["name"].lower()), (key, row))
    for key, row in rows.items():
        if row.get("repository"):
            continue
        found = known.get((group.get(row["ecosystem"], row["ecosystem"]), row["name"].lower()))
        if not found:
            continue
        other_key, other = found
        row["repository"] = other["repository"]
        row["source"] = f"same package recorded in {other_key} ({other['source']})"
        row["evidence_url"] = other.get("evidence_url")
        if other.get("verification"):
            row["verification"] = other["verification"]
        if other.get("directory"):
            row["directory"] = other["directory"]
        for k in ("repository_note", "homepage", "homepage_http", "captured_at_utc", "response_sha256"):
            row.pop(k, None)
        if not row.get("registry_url") and other.get("registry_url"):
            row["registry_url"] = other["registry_url"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="refetch every row")
    ap.add_argument("--offline", action="store_true", help="dry run on recorded facts only: no fetches, checks or writes")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    f = Fetcher(args.offline)
    previous = {}
    if OUT.exists() and not args.refresh:
        previous = json.loads(OUT.read_text()).get("rows", {})
    stars = {}
    for star in (load(STARS) or {}).get("rows", []):
        for p in star.get("paths", []):
            stars[p] = star
    plan = {}
    for cell in (load(PLAN) or {}).get("cells", []):
        for sel in cell.get("selected", []):
            plan[(cell["ecosystem"], cell["format"], sel["name"])] = sel
    cell_ctx = {}
    jobs = []
    for eco, fmt, row in rows_by_cell():
        if (eco, fmt) not in cell_ctx:
            base = ROOT / "data" / eco / fmt
            cell_ctx[(eco, fmt)] = (load(base / "source-lock.json"), load(base / "registry-snapshot.json"))
        lock, snap = cell_ctx[(eco, fmt)]
        jobs.append((eco, fmt, row, (lock, snap, stars, plan.get((eco, fmt, row["name"])))))

    def run(job):
        eco, fmt, row, ctx = job
        key = f"{eco}/{fmt}/{row['name']}"
        old = previous.get(key)
        if old and old.get("version") == str(row["version"]) and old.get("source") \
                and not old["source"].startswith("same package") and old.get("verification", {}).get("status") == 200:
            return key, old
        return key, resolve(f, eco, fmt, row, ctx)

    with ThreadPoolExecutor(args.workers) as pool:
        results = dict(pool.map(run, jobs))
    rows = {k: results[k] for k in sorted(results)}
    propagate(rows)
    summary = {}
    for row in rows.values():
        s = summary.setdefault(row["ecosystem"], {"rows": 0, "repository": 0, "null_with_note": 0})
        s["rows"] += 1
        s["repository" if row.get("repository") else "null_with_note"] += 1
    doc = {
        "schema_version": 1,
        "description": "Upstream source repository and registry page for every selected third-party parser path "
                       "in data/<ecosystem>/<format>/parsers.json. Written by "
                       "scripts/capture_upstream_repositories.py.",
        "policy": "Recorded repository facts first (parser record source fields, cell and project source locks, "
                  "GitHub supplemental star capture, cell registry snapshot); registry metadata fetched only to "
                  "fill gaps; a documentation URL on a code host is accepted last and only when the repository "
                  "name matches the package. No URL is guessed: rows without an established repository have "
                  "repository null and a repository_note. Recipe and port aggregators and Debian packaging "
                  "repositories are never treated as upstream.",
        "standard_apis": "Standard and runtime APIs (data/<ecosystem>/<format>/standard.json) are not linked here; "
                         "their records already carry official documentation URLs.",
        "summary": summary,
        "rows": rows,
    }
    if not args.offline:
        OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    bad = [k for k, r in rows.items() if r.get("repository") and r.get("verification", {}).get("status") != 200
           and not args.offline]
    print(json.dumps(summary, indent=1))
    if bad:
        print("unverified:", *bad, sep="\n  ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
