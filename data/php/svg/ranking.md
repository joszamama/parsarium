# PHP × SVG: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

Packagist lifetime package downloads.

| Rank | Package | Release | Packagist downloads (all time) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [dompdf/php-svg-lib](https://github.com/dompdf/php-svg-lib/blob/8259ffb930817e72b1ff1caef5d226501f3dfeb1/src/Svg/Document.php) | 1.0.2 | 80,006,827 | Root SVG dimensions; full raster rendering not exercised. | dompdf php-svg-lib XML/SVG parser |
| 2 | [enshrined/svg-sanitize](https://github.com/darylldoyle/svg-sanitizer/blob/1976ff93c8d8a234cdd3ff99626bd43ecf11bf49/README.md) | 1.1.1 | 55,204,366 | Valid two-rectangle SVG accepted by SVG sanitizer; parsed output retains rect and fill attributes. | enshrined SVG sanitizer over libxml DOM |
| 3 | [meyfa/php-svg](https://github.com/meyfa/php-svg/blob/a62c2b9842826e83ea51f9b9e6ed28d2bdb1033c/README.md) | v0.16.1 | 19,147,610 | One SVG document with two rectangle elements; no rasterization claim. | meyfa PHP-SVG typed document parser |
| 4 | [rhukster/dom-sanitizer](https://github.com/rhukster/dom-sanitizer/blob/83d618dac5aba78024d65983da1cc74514918e5f/README.md) | 1.0.20 | 4,025,649 | Valid two-rectangle SVG accepted with SVG-specific sanitizer profile. | Rhukster DOM/SVG sanitizer over libxml DOM |
| 5 | [darylldoyle/safe-svg](https://github.com/10up/safe-svg/blob/21a0fc4ea0515513d7e099603eb738b576109568/includes/safe-svg-sanitizer.php) | 2.5.2 | 337,362 | Standalone public helper replay with WordPress default option/filter behavior supplied by adapter; no full WordPress install claim. | enshrined SVG sanitizer over libxml DOM |
| 6 | [choowx/rasterize-svg](https://github.com/choowx/rasterize-svg/blob/d23fad7be783ebb15097e5abb31621223917ce9a/README.md) | v0.1.2 | 134,239 | Rendered simple two-rectangle SVG to 2 × 1 PNG; sharp 0.35.5 is pinned by repository package-lock.json. | sharp/libvips SVG renderer |
| 7 | [mathiasreker/php-svg-optimizer](https://github.com/MathiasReker/php-svg-optimizer/blob/16cdbb0f4193fc9f1d49f05d280946bf0e55a793/README.md) | 10.0.0 | 25,661 | One SVG document with two rectangles; first fill normalized from #ff0000 to red. | MathiasReker native PHP SVG optimizer over libxml DOM |
| 8 | [t3g/svg-sanitize-elts7](https://github.com/TYPO3GmbH/svg-sanitize-elts7/blob/3e6fcdfbcc74946c48b52244473033a2d9f36568/README.md) | 0.15.4.1 | 11,852 | Valid two-rectangle SVG on PHP 7.4; no full TYPO3 installation exercised. | enshrined SVG sanitizer over libxml DOM |
| 9 | [mediashowroom/php-svg](https://github.com/mediashowroom/php-svg/blob/ceaa17895593f5a744daf09890f5d036255c6d94/README.md) | v0.7.0 | 10,693 | Typed SVG document root and two direct rectangle child nodes. | mediashowroom PHP-SVG typed document parser |
| 10 | [bitandblack/image-information](https://bitbucket.org/wirbelwild/imageinformation/src/26a850670d6858740db1a506cb2197a5393e43c5/README.md) | 3.3.0 | 4,468 | SVG dimension reader only; PECL Imagick 3.8.1 parses via ImageMagick delegate. | ImageMagick SVG reader via PECL Imagick |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
