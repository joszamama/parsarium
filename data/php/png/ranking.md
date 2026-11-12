# PHP × PNG: verified parser ranking

7 verified third-party package paths; working goal 20, ceiling 30. The metric is Packagist package-level lifetime downloads, captured between 2026-11-12T09:39:46.746579+00:00 and 2026-11-12T09:44:13.460489+00:00. It counts all releases and all package uses, not just the PNG reading API. It is compared only within PHP. 0 path(s) lack a metric and remain unranked; equal counts share a rank.

Search hits and unresolved leads are separate from this ranking. PHP bundled APIs are listed in `standard.json` and do not enter the third-party ranking. Shared underlying parser families are recorded in `parsers.json`.

| Rank | Package | Pinned release | Lifetime downloads | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [intervention/image](https://github.com/Intervention/image/blob/3a47838f2e0f4ec6c8c9b43a5d73ac985b975830/readme.md) | 4.4.1 | 240,574,329 | decoded image dimensions | PHP GD PNG decoder |
| 2 | [imagine/imagine](https://github.com/php-imagine/Imagine/blob/dd57a4c290ff4d223d17bcd219dac9ac8bf1cc16/src/Gd/Imagine.php) | 1.5.4 | 81,891,624 | decoded image dimensions | PHP GD PNG decoder |
| 3 | [spatie/image](https://spatie.be/docs/image/v3/usage/basic-usage) | 3.9.10 | 74,942,530 | decoded image dimensions | PHP GD PNG decoder |
| 4 | [marc1706/fast-image-size](https://packagist.org/packages/marc1706/fast-image-size) | v1.3.1 | 9,796,811 | PNG dimensions and format type | FastImageSize PNG header reader |
| 5 | [gumlet/php-image-resize](https://github.com/gumlet/php-image-resize/blob/cd01c9e8aa2382211d760c825799c8102987a8c2/README.md) | 3.0.1 | 6,614,103 | decoded image dimensions | PHP GD PNG decoder |
| 6 | [gregwar/image](https://github.com/Gregwar/Image/blob/1cf64c34cbb22933b36727c16b15ed4d925b6fc6/Gregwar/Image/README.md) | v2.1.0 | 4,310,186 | decoded image dimensions | PHP GD PNG decoder |
| 7 | [claviska/simpleimage](https://github.com/claviska/SimpleImage/blob/f2397d67a06ed3334e5cfc22df55e55fb5f8bae1/README.md) | 4.4.2 | 2,510,200 | decoded dimensions and two RGB pixels | PHP GD PNG decoder |
