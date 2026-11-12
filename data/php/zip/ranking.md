# PHP × ZIP: verified parser ranking

8 verified third-party package paths; working goal 20, ceiling 30. The metric is Packagist package-level lifetime downloads, captured at 2026-11-12T09:14:24.797211+00:00. It counts all releases and all package uses, not just the ZIP reading API. It is compared only within PHP. 0 path(s) lack a metric and remain unranked; equal counts share a rank.

Search hits and unresolved leads are separate from this ranking. PHP bundled APIs are listed in `standard.json` and do not enter the third-party ranking. Several package paths delegate to PHP ZipArchive/libzip; see `family` and `family_note` in `parsers.json`.

| Rank | Package | Pinned release | Lifetime downloads | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [alchemy/zippy](https://github.com/alchemy-fr/Zippy/blob/3546ecd8ad5a1a1efb13315a5ea8ff1c7a1d5ef8/src/Zippy.php) | 2.0.0 | 24,569,178 | entry name and decompressed entry bytes | Alchemy Zippy wrapper over PHP ZipArchive |
| 2 | [pclzip/pclzip](https://github.com/ivanlanin/pclzip/blob/19dd1de9d3f5fc4d7d70175b4c344dee329f45fd/pclzip.lib.php) | 2.8.2 | 14,662,965 | entry name and decompressed entry bytes | PclZip PHP ZIP reader |
| 3 | [league/flysystem-ziparchive](https://github.com/thephpleague/flysystem-ziparchive/blob/ab6f9041b61ef517bc3e81891a4969181a39c17a/ZipArchiveAdapter.php) | 3.31.0 | 10,738,091 | entry name and decompressed entry bytes | Flysystem ZIP adapter over PHP ZipArchive |
| 4 | [nelexa/zip](https://github.com/Ne-Lexa/php-zip/blob/88a1b6549be813278ff2dd3b6b2ac188827634a7/README.md) | 4.0.2 | 9,029,158 | entry name and decompressed entry bytes | Ne-Lexa pure PHP ZIP reader |
| 5 | [wapmorgan/unified-archive](https://github.com/wapmorgan/UnifiedArchive/blob/2097cdf0995f4a576773d66803af4245ed55636e/docs/API.md) | 1.3.1 | 1,991,032 | entry name and decompressed entry bytes | UnifiedArchive ZIP driver over PHP ZipArchive |
| 6 | [splitbrain/php-archive](https://github.com/splitbrain/php-archive/blob/0d8801eaac5342b26ff1776089d4a124117b652c/README.md) | 1.5.1 | 1,785,396 | entry name and decompressed entry bytes | splitbrain PHP ZIP reader |
| 7 | [vipsoft/unzip](https://github.com/vipsoft/Unzip/blob/090712dc65d0d77842f077d0a768fc7c852d4624/README.md) | 1.3 | 1,473,735 | entry name and decompressed entry bytes | VIPSoft wrapper over PHP ZipArchive |
| 8 | [comodojo/zip](https://github.com/comodojo/zip/blob/22e11bda2ab8e1057cf4d1a50a98ab22f9e38e34/src/Comodojo/Zip/Zip.php) | 3.1.1 | 479,706 | entry name and decompressed entry bytes | Comodojo wrapper over PHP ZipArchive |
