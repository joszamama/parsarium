# PYTHON × ZIP: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

PyPI Stats last_month downloads excluding known mirrors.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [fsspec](https://filesystem-spec.readthedocs.io/en/latest/api.html#fsspec.implementations.zip.ZipFileSystem) | 2026.9.0 | 556,880,889 | DEFLATE ZIP entry name and content | fsspec ZipFileSystem via CPython zipfile |
| 2 | [zipp](https://zipp.readthedocs.io/en/latest/) | 4.1.2 | 366,031,309 | DEFLATE ZIP entry name and content | zipp via CPython zipfile |
| 3 | [pyzipper](https://pypi.org/project/pyzipper/0.4.0/) | 0.4.0 | 7,278,260 | DEFLATE ZIP entry name and content | pyzipper fork of CPython zipfile 3.7 |
| 4 | [zipfile-zstd](https://pypi.org/project/zipfile-zstd/0.0.4/) | 0.0.4 | 2,907,691 | Zstandard ZIP method 93 entry name and content | CPython zipfile plus zstandard codec |
| 5 | [fs](https://github.com/PyFilesystem/pyfilesystem2/blob/master/fs/zipfs.py) | 2.4.16 | 1,534,623 | DEFLATE ZIP entry name and content | PyFilesystem ZipFS via CPython zipfile |
| 6 | [zipfile36](https://pypi.org/project/zipfile36/0.1.3/) | 0.1.3 | 1,149,613 | DEFLATE ZIP entry name and content | CPython zipfile 3.6 backport |
| 7 | [stream-unzip](https://github.com/uktrade/stream-unzip) | 0.0.101 | 815,475 | DEFLATE ZIP entry name and content | stream-unzip native Python parser |
| 8 | [patool](https://pypi.org/project/patool/4.1.0/) | 4.1.0 | 810,100 | DEFLATE ZIP entry name and content | patool via local unzip utility |
| 9 | [libarchive-c](https://github.com/Changaco/python-libarchive-c) | 5.3 | 441,734 | DEFLATE ZIP entry name and content | native libarchive |
| 10 | [pyunpack](https://pypi.org/project/pyunpack/0.3/) | 0.3 | 194,489 | DEFLATE ZIP entry name and content | pyunpack via CPython zipfile |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
