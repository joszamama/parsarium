"""Check the YAML controls against hand-written expected typed trees.

The two controls are hand-written YAML 1.2 documents, one document per file,
UTF-8 without a BOM, with no tabs in indentation, no %YAML directive, no tags
and no merge keys. Every plain scalar resolves to the same type under the YAML
1.1 resolvers (PyYAML, libyaml-based loaders, SnakeYAML, go-yaml v2 style) and
the YAML 1.2 core schema: no yes/no/on/off/y/n, no leading-zero or 0o/0x/0b
integers, no sexagesimal numbers, no exponent without a dot, no timestamps,
no `<<` or `=`. A plain-looking string that would resolve differently, such as
the ZIP code "10115", is double-quoted.

The oracle is the hand-written EXPECTED tree below. It is checked three ways:
1. the control hashes are pinned;
2. every string in the tree that a YAML 1.1 or 1.2 core resolver would read as
   a non-string must appear quoted in the source;
3. when a Ruby with Psych is on PATH, Psych.safe_load (libyaml family; the same
   family as C libyaml, PyYAML's CLoader and PHP ext-yaml, but not counted in
   any Parsarium cell) must produce the same typed tree. Pass --require-psych
   to fail when Ruby is unavailable.

Tree encoding (shared by every harness): ["map", [[key, node], ...]] in source
order, ["seq", [node, ...]], ["str", text], ["int", decimal text],
["float", shortest round-trip decimal text], ["bool", true|false], ["null"].
Aliases are expanded; anchors are not reported.
"""

from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
CONTROLS = {
    "catalog.yaml": "b574210db4f284734fe62b59833b24f53c99e6b5948d9d5e379f1c1439ac8d5d",
    "order.yaml": "a7d81a704bf582a1f54b1bcb4dfe1c68a62718e5cfc3196ccd406e4ec36bc935",
}


def s(text):
    return ["str", text]


def i(value):
    return ["int", str(value)]


def f(text):
    return ["float", text]


def m(*pairs):
    return ["map", [[key, node] for key, node in pairs]]


def q(*nodes):
    return ["seq", list(nodes)]


BASE = m(("retries", i(3)), ("label", s("base")))
SHARED = m(("city", s("Berlin")), ("zip", s("10115")))
EXPECTED = {
    "catalog.yaml": m(
        ("kind", s("catalog")),
        ("version", i(2)),
        ("ratio", f("0.25")),
        ("offset", i(-17)),
        ("enabled", ["bool", True]),
        ("retired", ["bool", False]),
        ("missing", ["null"]),
        ("title", s('Café "quoted"\tend')),
        ("single", s("it's here")),
        ("tags", q(s("alpha"), s("beta"), s("gamma delta"))),
        ("point", m(("lat", i(1)), ("lon", f("-2.5")))),
        ("items", q(
            m(("id", i(7)), ("name", s("first item")), ("note", s("line one\nline two\n"))),
            m(("id", i(8)), ("name", s("Zürich")), ("note", s("folded text\n"))),
        )),
        ("defaults", BASE),
        ("service", m(("settings", BASE), ("label", s("edge")))),
    ),
    "order.yaml": q(
        m(("order", s("A-7")),
          ("lines", q(
              m(("sku", s("Xé-1")), ("qty", i(2)), ("price", f("12.5"))),
              m(("sku", s("B '2'")), ("qty", i(1)), ("price", f("0.75"))),
          )),
          ("flags", q()),
          ("meta", m())),
        SHARED,
        SHARED,
        q(i(1), q(i(2), i(3)), m(("k", s("v")))),
        s("plain multi word"),
        s("line\nbreak"),
        s("kept\n  indented"),
        ["null"],
        ["bool", False],
    ),
}

# Plain-scalar patterns that a YAML 1.1 or YAML 1.2 core resolver types as non-strings.
NON_STRING = [re.compile(pattern) for pattern in (
    r"(?i:y|yes|n|no|true|false|on|off)",
    r"(?:~|null|Null|NULL|)",
    r"[-+]?(?:0|[1-9][0-9_]*)",
    r"[-+]?0[0-7_]+|0o[0-7]+|0x[0-9a-fA-F_]+|0b[01_]+",
    r"[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+(?:\.[0-9_]*)?",
    r"[-+]?(?:\.[0-9]+|[0-9][0-9_]*(?:\.[0-9_]*)?)(?:[eE][-+]?[0-9]+)?",
    r"[-+]?\.(?:inf|Inf|INF)|\.(?:nan|NaN|NAN)",
    r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}.*",
    r"<<|=",
)]


def walk(node, path="$"):
    yield path, node
    if node[0] == "map":
        for key, value in node[1]:
            yield path + "." + key, ["str", key]
            yield from walk(value, path + "." + key)
    elif node[0] == "seq":
        for index, value in enumerate(node[1]):
            yield from walk(value, f"{path}[{index}]")


def summary(tree) -> dict:
    """Node counts by kind and the maximum container depth of one typed tree."""
    counts: dict[str, int] = {}

    def visit(node, depth):
        counts[node[0]] = counts.get(node[0], 0) + 1
        if node[0] == "map":
            return max([depth] + [visit(value, depth + 1) for _, value in node[1]])
        if node[0] == "seq":
            return max([depth] + [visit(value, depth + 1) for value in node[1]])
        return depth - 1

    depth = visit(tree, 1)
    return {"root": tree[0], "nodes": dict(sorted(counts.items())), "max_depth": depth}


def tree_sha256(tree) -> str:
    return sha256(json.dumps(tree, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


PSYCH = r"""
require "psych"; require "json"
def t(v)
  case v
  when Hash then ["map", v.map { |k, x| [k, t(x)] }]
  when Array then ["seq", v.map { |x| t(x) }]
  when String then ["str", v]
  when Integer then ["int", v.to_s]
  when Float then ["float", v.to_s]
  when true, false then ["bool", v]
  when nil then ["null"]
  else raise "unexpected #{v.class}"
  end
end
docs = Psych.parse_stream(File.read(ARGV[0], encoding: "UTF-8")).children
raise "expected one document" unless docs.length == 1
puts JSON.generate({"psych" => Psych::VERSION, "libyaml" => Psych::LIBYAML_VERSION,
                    "tree" => t(Psych.safe_load(File.read(ARGV[0], encoding: "UTF-8"), aliases: true))})
"""


def psych_tree(path: Path):
    ruby = shutil.which("ruby")
    if not ruby:
        return None
    result = subprocess.run([ruby, "-e", PSYCH, str(path)], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def check(require_psych: bool = False) -> dict:
    report = {}
    for name, digest in CONTROLS.items():
        path = ROOT / name
        data = path.read_bytes()
        if sha256(data).hexdigest() != digest:
            raise SystemExit(f"{name}: control hash changed")
        text = data.decode("utf-8")
        if text.startswith("﻿") or "\t" in text or "\r" in text or "%YAML" in text or "<<" in text:
            raise SystemExit(f"{name}: BOM, tab, CR, directive or merge key present")
        tree = EXPECTED[name]
        for path_name, node in walk(tree):
            if node[0] == "str" and any(p.fullmatch(node[1]) for p in NON_STRING):
                if f'"{node[1]}"' not in text and f"'{node[1]}'" not in text:
                    raise SystemExit(f"{name}: {path_name} {node[1]!r} is schema-ambiguous and unquoted")
        observed = psych_tree(path)
        if observed is None and require_psych:
            raise SystemExit("ruby with Psych is required")
        if observed is not None and observed["tree"] != tree:
            raise SystemExit(f"{name}: Psych tree differs from the expected tree")
        report[name] = {"sha256": digest, "bytes": len(data), "tree_sha256": tree_sha256(tree),
                        **summary(tree),
                        "psych_cross_check": None if observed is None else
                        {"psych": observed["psych"], "libyaml": observed["libyaml"], "match": True}}
    return report


if __name__ == "__main__":
    print(json.dumps(check("--require-psych" in sys.argv[1:]), indent=2, ensure_ascii=False))
