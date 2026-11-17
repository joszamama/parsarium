"""Require executed rapidyaml parse-engine regions in the _ryml extension; export Parsarium source lines.

Counted scope: the C++ rapidyaml 0.15.2 sources under cpp/src/c4/yml/ (parse engine, tree,
reference resolver). c4core helpers under cpp/ext/c4core/src/c4/ are reported separately, and
the SWIG-generated wrapper is not counted.
"""
import json
from pathlib import Path

root = Path('/coverage')
raw = json.loads((root / 'native.json').read_text())
prefix = '/work/ryml-src/cpp/src/c4/yml/'
support = '/work/ryml-src/cpp/ext/c4core/src/c4/'


def executed(item):
    return sorted({line for line, column, count, has_count, region_entry, *_ in item['segments']
                   if has_count and region_entry and count > 0})


files, helpers = [], []
for item in raw['data'][0]['files']:
    filename = item['filename']
    lines = executed(item)
    if not lines:
        continue
    record = {'filename': filename, 'summary': {'lines': {'covered': len(lines)}}, 'executed_lines': lines}
    if filename.startswith(prefix):
        files.append(record)
    elif filename.startswith(support):
        helpers.append(record)
for required in ('parse_engine.def.hpp', 'tree.cpp', 'reference_resolver.cpp'):
    if not any(item['filename'] == prefix + required for item in files):
        raise SystemExit(f'{required} had no executed source regions')
for unused in ('emit.def.hpp', 'writer.hpp'):
    if any(item['filename'] == prefix + unused for item in files):
        raise SystemExit(f'{unused} executed during a parse')
observed = json.loads((root / 'observed.json').read_text())
coverage = {'data': [{'files': files + helpers}]}
summary = {'control_pass': True, 'output': observed, 'parser_source_files': len(files),
           'parser_source_lines_covered': sum(len(item['executed_lines']) for item in files),
           'dependency_source_files': len(helpers),
           'dependency_source_lines_covered': sum(len(item['executed_lines']) for item in helpers),
           'coverage': '/coverage/coverage.json'}
(root / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
(root / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
