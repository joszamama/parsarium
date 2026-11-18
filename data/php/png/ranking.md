# PHP × PNG: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

Packagist package lifetime downloads, all versions.

| Rank | Package | Release | Packagist downloads (all time) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [nette/utils](https://github.com/nette/utils/blob/6bf24518accf32cf845bca305e0b92078700fd01/src/Utils/Image.php) | v4.1.6 | 510,750,784 | decoded dimensions and PNG type | PHP GD PNG decoder |
| 2 | [intervention/image](https://github.com/Intervention/image/blob/3a47838f2e0f4ec6c8c9b43a5d73ac985b975830/readme.md) | 4.4.1 | 240,574,329 | decoded image dimensions | PHP GD PNG decoder |
| 3 | [imagine/imagine](https://github.com/php-imagine/Imagine/blob/dd57a4c290ff4d223d17bcd219dac9ac8bf1cc16/src/Gd/Imagine.php) | 1.5.4 | 81,891,624 | decoded image dimensions | PHP GD PNG decoder |
| 4 | [spatie/image](https://spatie.be/docs/image/v3/usage/basic-usage) | 3.9.10 | 74,942,530 | decoded image dimensions | PHP GD PNG decoder |
| 5 | [league/glide](https://github.com/thephpleague/glide/blob/54643c4c55ce6dc7f8a11d9c643340051d54c4d9/src/ServerFactory.php) | 4.1.0 | 57,155,709 | decoded and re-encoded PNG dimensions | Intervention Image / PHP GD PNG decoder |
| 6 | [intervention/image-laravel](https://github.com/Intervention/image-laravel/blob/8a8bd2c7bb4a9aa2b046ff066fd1cd44b1de0da2/src/Facades/Image.php) | 4.1.1 | 14,165,052 | decoded image dimensions | Intervention Image 4 / PHP GD PNG decoder |
| 7 | [marc1706/fast-image-size](https://packagist.org/packages/marc1706/fast-image-size) | v1.3.1 | 9,796,811 | PNG dimensions and format type | FastImageSize PNG header reader |
| 8 | [rosell-dk/webp-convert](https://github.com/rosell-dk/webp-convert/blob/bce87de61cff098e899a91960f9fdb08e8867194/README.md) | 2.9.5 | 9,509,668 | PNG decoded to WebP with dimensions | PHP GD PNG decoder |
| 9 | [gumlet/php-image-resize](https://github.com/gumlet/php-image-resize/blob/cd01c9e8aa2382211d760c825799c8102987a8c2/README.md) | 3.0.1 | 6,614,103 | decoded image dimensions | PHP GD PNG decoder |
| 10 | [yiisoft/yii2-imagine](https://github.com/yiisoft/yii2-imagine/blob/7ec4332dc25893aec5a7cf084722b162b3a4d55d/src/BaseImage.php) | 2.3.1 | 6,010,850 | decoded PNG dimensions after thumbnail | Imagine / PHP GD PNG decoder |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
