# PHP × ASCII PNM: verified parser ranking

14 verified third-party package paths; working goal 20, original ceiling 30. Packagist lifetime package downloads were captured at 2026-11-12T16:32:33.197093+00:00 for the 13 Composer paths. Counts cover all releases and formats, and rank adoption signals only within PHP. PECL Imagick has no comparable metric and remains unranked.

Six paths share the libvips PPM loader. Eight paths use ImageMagick decoding through PECL Imagick or the CLI. The control is one valid ASCII P3 image; passing it does not establish support for every PNM variant. Search hits and unresolved leads are in `registry-snapshot.json` and `leads.json`.

| Rank | Package | Pinned release | Lifetime Composer downloads | Observable scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [intervention/image](https://packagist.org/packages/intervention/image#4.4.1) | 4.4.1 | 240,839,091 | decoded image dimensions | libvips PPM/PNM decoder |
| 2 | [imagine/imagine](https://packagist.org/packages/imagine/imagine#1.5.4) | 1.5.4 | 81,891,624 | decoded image dimensions | ImageMagick PNM decoder |
| 3 | [spatie/image](https://packagist.org/packages/spatie/image#3.9.10) | 3.9.10 | 74,942,530 | decoded image dimensions | libvips PPM/PNM decoder |
| 4 | [league/glide](https://packagist.org/packages/league/glide#4.2.0) | 4.2.0 | 57,155,709 | converted PNG dimensions and MIME | ImageMagick PNM decoder |
| 5 | [jcupitt/vips](https://packagist.org/packages/jcupitt/vips#v2.6.1) | v2.6.1 | 2,819,505 | decoded dimensions and RGB pixels | libvips PPM/PNM decoder |
| 6 | [calcinai/php-imagick](https://packagist.org/packages/calcinai/php-imagick#v0.1.2) | v0.1.2 | 963,050 | decoded P6 dimensions and RGB pixels | ImageMagick PNM decoder |
| 7 | [rokka/imagine-vips](https://packagist.org/packages/rokka/imagine-vips#0.42.0) | 0.42.0 | 781,370 | decoded image dimensions | libvips PPM/PNM decoder |
| 8 | [orbitale/imagemagick-php](https://packagist.org/packages/orbitale/imagemagick-php#v3.3.5) | v3.3.5 | 462,023 | identified PPM type and dimensions | ImageMagick PNM decoder |
| 9 | [intervention/image-driver-vips](https://packagist.org/packages/intervention/image-driver-vips#4.2.0) | 4.2.0 | 441,145 | decoded image dimensions | libvips PPM/PNM decoder |
| 10 | [francodacosta/phmagick](https://packagist.org/packages/francodacosta/phmagick#v5.0.2) | v5.0.2 | 74,152 | converted PNG dimensions and MIME | ImageMagick PNM decoder |
| 11 | [osiemsiedem/intervention-image-vips-driver](https://packagist.org/packages/osiemsiedem/intervention-image-vips-driver#v0.11.0) | v0.11.0 | 64,537 | decoded image dimensions | libvips PPM/PNM decoder |
| 12 | [phpixie/image](https://packagist.org/packages/phpixie/image#3.3) | 3.3 | 58,216 | decoded image dimensions | ImageMagick PNM decoder |
| 13 | [phpthumb/phpthumb](https://packagist.org/packages/phpthumb/phpthumb#2.5.1) | 2.5.1 | 18,743 | decoded image dimensions | ImageMagick PNM decoder |
| — | [pecl/imagick](https://pecl.php.net/package/imagick/3.8.1) | 3.8.1 | unavailable | decoded dimensions and RGB pixels | ImageMagick PNM decoder |
