# PHP × ZIP: verified parser ranking

20 verified third-party package paths; working goal 20, ceiling 30. The metric is Packagist package-level lifetime downloads, captured between 2026-11-12T09:14:24.797211+00:00 and 2026-11-12T09:34:57.143943+00:00. It counts all releases and all package uses, not just the ZIP reading API. It is compared only within PHP. 0 path(s) lack a metric and remain unranked; equal counts share a rank.

Search hits and unresolved leads are separate from this ranking. PHP bundled APIs are listed in `standard.json` and do not enter the third-party ranking. Several package paths delegate to PHP ZipArchive/libzip; see `family` and `family_note` in `parsers.json`.

| Rank | Package | Pinned release | Lifetime downloads | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [alchemy/zippy](https://github.com/alchemy-fr/Zippy/blob/3546ecd8ad5a1a1efb13315a5ea8ff1c7a1d5ef8/src/Zippy.php) | 2.0.0 | 24,569,178 | entry name and decompressed entry bytes | Alchemy Zippy wrapper over PHP ZipArchive |
| 2 | [pclzip/pclzip](https://github.com/ivanlanin/pclzip/blob/19dd1de9d3f5fc4d7d70175b4c344dee329f45fd/pclzip.lib.php) | 2.8.2 | 14,662,965 | entry name and decompressed entry bytes | PclZip PHP ZIP reader |
| 3 | [league/flysystem-ziparchive](https://github.com/thephpleague/flysystem-ziparchive/blob/ab6f9041b61ef517bc3e81891a4969181a39c17a/ZipArchiveAdapter.php) | 3.31.0 | 10,738,091 | entry name and decompressed entry bytes | Flysystem ZIP adapter over PHP ZipArchive |
| 4 | [nelexa/zip](https://github.com/Ne-Lexa/php-zip/blob/88a1b6549be813278ff2dd3b6b2ac188827634a7/README.md) | 4.0.2 | 9,029,158 | entry name and decompressed entry bytes | Ne-Lexa pure PHP ZIP reader |
| 5 | [chumper/zipper](https://github.com/Chumper/Zipper/blob/d15207e010f8fe1bdd341376bd86d599c4166423/README.md) | v1.0.3 | 4,665,985 | decompressed bytes of a named entry | Chumper Zipper over PHP ZipArchive |
| 6 | [zanysoft/laravel-zip](https://github.com/zanysoft/laravel-zip/blob/ee2a4f44a0236bab8e223c0eb8c4c8b6c739cb9b/README.md) | 3.1.0 | 3,249,533 | entry name and decompressed entry bytes | ZanySoft ZIP wrapper over PHP ZipArchive |
| 7 | [matomo/decompress](https://github.com/matomo-org/component-decompress/blob/3e96938cd11f90e5e4bcc38c78264c86a63f41bb/README.md) | 3.0.0 | 2,943,212 | entry name and decompressed entry bytes | Matomo extractor over PHP ZipArchive |
| 8 | [madnest/madzipper](https://github.com/madnest/madzipper/blob/527c35105820a0b4c8cfdadd3f475b26d62d9ac2/README.md) | 1.6.0 | 2,822,664 | entry name and decompressed entry bytes | Madnest Madzipper over PHP ZipArchive |
| 9 | [wapmorgan/unified-archive](https://github.com/wapmorgan/UnifiedArchive/blob/2097cdf0995f4a576773d66803af4245ed55636e/docs/API.md) | 1.3.1 | 1,991,032 | entry name and decompressed entry bytes | UnifiedArchive ZIP driver over PHP ZipArchive |
| 10 | [splitbrain/php-archive](https://github.com/splitbrain/php-archive/blob/0d8801eaac5342b26ff1776089d4a124117b652c/README.md) | 1.5.1 | 1,785,396 | entry name and decompressed entry bytes | splitbrain PHP ZIP reader |
| 11 | [vipsoft/unzip](https://github.com/vipsoft/Unzip/blob/090712dc65d0d77842f077d0a768fc7c852d4624/README.md) | 1.3 | 1,473,735 | entry name and decompressed entry bytes | VIPSoft wrapper over PHP ZipArchive |
| 12 | [zetacomponents/archive](https://zetacomponents.org/documentation/trunk/Archive/tutorial.html) | 1.5.1 | 509,571 | entry name and decompressed entry bytes | Zeta Components custom PHP ZIP reader |
| 13 | [comodojo/zip](https://github.com/comodojo/zip/blob/22e11bda2ab8e1057cf4d1a50a98ab22f9e38e34/src/Comodojo/Zip/Zip.php) | 3.1.1 | 479,706 | entry name and decompressed entry bytes | Comodojo wrapper over PHP ZipArchive |
| 14 | [joomla/archive](https://github.com/joomla-framework/archive/blob/7a8d0eda637bd37bc3de744aa3e4ce516d4356b0/README.md) | 4.0.0 | 450,574 | entry name and decompressed entry bytes | Joomla ZIP adapter over PHP ZipArchive |
| 15 | [macellan/laravel-zip](https://github.com/macellan/laravel-zip/blob/0c40d22de710acb5e4da8620663fb336741cdc5d/README.md) | 1.0.5 | 270,070 | entry name and decompressed entry bytes | Macellan fork of ZanySoft over PHP ZipArchive |
| 16 | [chamilo/pclzip](https://github.com/chamilo/pclzip/blob/af10d07a39922b0789bf761524a22ecefc01d405/readme.txt) | v2.8.5 | 180,805 | entry name and decompressed entry bytes | Chamilo PclZip fork |
| 17 | [mmoreram/extractor](https://github.com/mmoreram/extractor/blob/0ca76992fab2573e2fe512d0ee2a4d45e936fee4/README.md) | 1.2.1 | 137,579 | entry name and decompressed entry bytes | Mmoreram extractor over PHP ZipArchive |
| 18 | [kiwilan/php-archive](https://github.com/kiwilan/php-archive/blob/2e202603396a620720aad676c4037eebc0443090/README.md) | 2.3.02 | 45,598 | entry name and decompressed entry bytes | Kiwilan archive wrapper over PHP ZipArchive |
| 19 | [seblucas/tbszip](https://github.com/seblucas/tbszip/blob/2c50bf309bb4431a24e206f164fdb4a2e6b10b7f/README.md) | 2.16.1 | 22,409 | entry name and decompressed entry bytes | TbsZip custom PHP ZIP reader |
| 20 | [smuuf/zip-reader](https://github.com/smuuf/php-zip-reader/blob/363eaa22a52be72a2dc3fc6c3bef78835da4f259/README.md) | 1.0 | 49 | entry name and decompressed entry bytes | Smuuf ZIP reader over PHP ZipArchive |
