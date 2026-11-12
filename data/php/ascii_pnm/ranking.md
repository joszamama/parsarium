# PHP × ASCII PNM: verified parser ranking

8 verified third-party package paths; working goal 20, original ceiling 30. Packagist lifetime package downloads were captured at 2026-11-12T16:14:47.502626+00:00 for the seven Composer paths. Counts cover all releases and formats, and rank adoption signals only within PHP. PECL Imagick has no comparable metric and remains unranked.

Six paths share the libvips PPM loader. Imagine and PECL Imagick share ImageMagick decoding. The control is one valid ASCII P3 image; passing it does not establish support for every PNM variant. Search hits and unresolved leads are in `registry-snapshot.json` and `leads.json`.

| Rank | Package | Pinned release | Lifetime Composer downloads | Observable scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [intervention/image](https://packagist.org/packages/intervention/image#4.4.1) | 4.4.1 | 240,839,091 | decoded image dimensions | libvips PPM/PNM decoder |
| 2 | [imagine/imagine](https://packagist.org/packages/imagine/imagine#1.5.4) | 1.5.4 | 81,891,624 | decoded image dimensions | ImageMagick PNM decoder |
| 3 | [spatie/image](https://packagist.org/packages/spatie/image#3.9.10) | 3.9.10 | 74,942,530 | decoded image dimensions | libvips PPM/PNM decoder |
| 4 | [jcupitt/vips](https://packagist.org/packages/jcupitt/vips#v2.6.1) | v2.6.1 | 2,819,505 | decoded dimensions and RGB pixels | libvips PPM/PNM decoder |
| 5 | [rokka/imagine-vips](https://packagist.org/packages/rokka/imagine-vips#0.42.0) | 0.42.0 | 781,370 | decoded image dimensions | libvips PPM/PNM decoder |
| 6 | [intervention/image-driver-vips](https://packagist.org/packages/intervention/image-driver-vips#4.2.0) | 4.2.0 | 441,145 | decoded image dimensions | libvips PPM/PNM decoder |
| 7 | [osiemsiedem/intervention-image-vips-driver](https://packagist.org/packages/osiemsiedem/intervention-image-vips-driver#v0.11.0) | v0.11.0 | 64,537 | decoded image dimensions | libvips PPM/PNM decoder |
| — | [pecl/imagick](https://pecl.php.net/package/imagick/3.8.1) | 3.8.1 | unavailable | decoded dimensions and RGB pixels | ImageMagick PNM decoder |
