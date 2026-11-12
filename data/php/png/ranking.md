# PHP × PNG: verified parser ranking

11 verified third-party package paths; working goal 20, ceiling 30. The metric is Packagist package-level lifetime downloads, captured between 2026-11-12T09:39:46.746579+00:00 and 2026-11-12T09:49:18.788552+00:00. It counts all releases and all package uses, not just the PNG reading API. It is compared only within PHP. 0 path(s) lack a metric and remain unranked; equal counts share a rank.

Search hits and unresolved leads are separate from this ranking. PHP bundled APIs are listed in `standard.json` and do not enter the third-party ranking. Shared underlying parser families are recorded in `parsers.json`.

| Rank | Package | Pinned release | Lifetime downloads | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [intervention/image](https://github.com/Intervention/image/blob/3a47838f2e0f4ec6c8c9b43a5d73ac985b975830/readme.md) | 4.4.1 | 240,574,329 | decoded image dimensions | PHP GD PNG decoder |
| 2 | [imagine/imagine](https://github.com/php-imagine/Imagine/blob/dd57a4c290ff4d223d17bcd219dac9ac8bf1cc16/src/Gd/Imagine.php) | 1.5.4 | 81,891,624 | decoded image dimensions | PHP GD PNG decoder |
| 3 | [spatie/image](https://spatie.be/docs/image/v3/usage/basic-usage) | 3.9.10 | 74,942,530 | decoded image dimensions | PHP GD PNG decoder |
| 4 | [league/glide](https://github.com/thephpleague/glide/blob/54643c4c55ce6dc7f8a11d9c643340051d54c4d9/src/ServerFactory.php) | 4.1.0 | 57,155,709 | decoded and re-encoded PNG dimensions | Intervention Image / PHP GD PNG decoder |
| 5 | [marc1706/fast-image-size](https://packagist.org/packages/marc1706/fast-image-size) | v1.3.1 | 9,796,811 | PNG dimensions and format type | FastImageSize PNG header reader |
| 6 | [rosell-dk/webp-convert](https://github.com/rosell-dk/webp-convert/blob/bce87de61cff098e899a91960f9fdb08e8867194/README.md) | 2.9.5 | 9,509,668 | PNG decoded to WebP with dimensions | PHP GD PNG decoder |
| 7 | [gumlet/php-image-resize](https://github.com/gumlet/php-image-resize/blob/cd01c9e8aa2382211d760c825799c8102987a8c2/README.md) | 3.0.1 | 6,614,103 | decoded image dimensions | PHP GD PNG decoder |
| 8 | [league/color-extractor](https://github.com/thephpleague/color-extractor/blob/21fcac6249c5ef7d00eb83e128743ee6678fe505/README.md) | 0.4.0 | 5,850,208 | decoded pixel color histogram | PHP GD PNG decoder |
| 9 | [gregwar/image](https://github.com/Gregwar/Image/blob/1cf64c34cbb22933b36727c16b15ed4d925b6fc6/Gregwar/Image/README.md) | v2.1.0 | 4,310,186 | decoded image dimensions | PHP GD PNG decoder |
| 10 | [jcupitt/vips](https://github.com/libvips/php-vips/blob/6dbba1bb3a4ba1e39edb71016a2aa6da5bff32ee/README.md) | v2.6.1 | 2,811,421 | decoded image dimensions | libvips PNG decoder |
| 11 | [claviska/simpleimage](https://github.com/claviska/SimpleImage/blob/f2397d67a06ed3334e5cfc22df55e55fb5f8bae1/README.md) | 4.4.2 | 2,510,200 | decoded dimensions and two RGB pixels | PHP GD PNG decoder |
