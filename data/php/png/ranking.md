# PHP × PNG: verified parser ranking

3 verified third-party package paths; working goal 20, ceiling 30. The metric is Packagist package-level lifetime downloads, captured at 2026-11-12T09:39:46.746579+00:00. It counts all releases and all package uses, not just the PNG reading API. It is compared only within PHP. 0 path(s) lack a metric and remain unranked; equal counts share a rank.

Search hits and unresolved leads are separate from this ranking. PHP bundled APIs are listed in `standard.json` and do not enter the third-party ranking. Shared underlying parser families are recorded in `parsers.json`.

| Rank | Package | Pinned release | Lifetime downloads | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [intervention/image](https://github.com/Intervention/image/blob/3a47838f2e0f4ec6c8c9b43a5d73ac985b975830/readme.md) | 4.4.1 | 240,574,329 | decoded image dimensions | PHP GD PNG decoder |
| 2 | [imagine/imagine](https://github.com/php-imagine/Imagine/blob/dd57a4c290ff4d223d17bcd219dac9ac8bf1cc16/src/Gd/Imagine.php) | 1.5.4 | 81,891,624 | decoded image dimensions | PHP GD PNG decoder |
| 3 | [claviska/simpleimage](https://github.com/claviska/SimpleImage/blob/f2397d67a06ed3334e5cfc22df55e55fb5f8bae1/README.md) | 4.4.2 | 2,510,200 | decoded dimensions and two RGB pixels | PHP GD PNG decoder |
