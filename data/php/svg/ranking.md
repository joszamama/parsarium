# PHP × SVG: verified parser ranking

20 pinned third-party package paths passed valid local SVG controls; working goal 20, original ceiling 30. Packagist lifetime downloads were captured with the bounded search snapshot at 2026-11-12T18:57:06.401152+00:00. This metric covers all package uses and is comparable only within PHP. 6 named leads remain unresolved, so the list is not a definitive most-used top twenty.

| Rank | Package | Pinned release | Lifetime downloads | Observable scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [dompdf/php-svg-lib](https://packagist.org/packages/dompdf/php-svg-lib#1.0.2) | 1.0.2 | 80,006,827 | Root SVG dimensions; full raster rendering not exercised. | dompdf php-svg-lib XML/SVG parser |
| 2 | [enshrined/svg-sanitize](https://packagist.org/packages/enshrined/svg-sanitize#1.1.1) | 1.1.1 | 55,204,366 | Valid two-rectangle SVG accepted by SVG sanitizer; parsed output retains rect and fill attributes. | enshrined SVG sanitizer over libxml DOM |
| 3 | [meyfa/php-svg](https://packagist.org/packages/meyfa/php-svg#v0.16.1) | v0.16.1 | 19,147,610 | One SVG document with two rectangle elements; no rasterization claim. | meyfa PHP-SVG typed document parser |
| 4 | [rhukster/dom-sanitizer](https://packagist.org/packages/rhukster/dom-sanitizer#1.0.20) | 1.0.20 | 4,025,649 | Valid two-rectangle SVG accepted with SVG-specific sanitizer profile. | Rhukster DOM/SVG sanitizer over libxml DOM |
| 5 | [darylldoyle/safe-svg](https://packagist.org/packages/darylldoyle/safe-svg#2.5.2) | 2.5.2 | 337,362 | Standalone public helper replay with WordPress default option/filter behavior supplied by adapter; no full WordPress install claim. | enshrined SVG sanitizer over libxml DOM |
| 6 | [choowx/rasterize-svg](https://packagist.org/packages/choowx/rasterize-svg#v0.1.2) | v0.1.2 | 134,239 | Rendered simple two-rectangle SVG to 2 × 1 PNG; sharp 0.35.5 is pinned by repository package-lock.json. | sharp/libvips SVG renderer |
| 7 | [mathiasreker/php-svg-optimizer](https://packagist.org/packages/mathiasreker/php-svg-optimizer#10.0.0) | 10.0.0 | 25,661 | One SVG document with two rectangles; first fill normalized from #ff0000 to red. | MathiasReker native PHP SVG optimizer over libxml DOM |
| 8 | [t3g/svg-sanitize-elts7](https://packagist.org/packages/t3g/svg-sanitize-elts7#0.15.4.1) | 0.15.4.1 | 11,852 | Valid two-rectangle SVG on PHP 7.4; no full TYPO3 installation exercised. | enshrined SVG sanitizer over libxml DOM |
| 9 | [mediashowroom/php-svg](https://packagist.org/packages/mediashowroom/php-svg#v0.7.0) | v0.7.0 | 10,693 | Typed SVG document root and two direct rectangle child nodes. | mediashowroom PHP-SVG typed document parser |
| 10 | [bitandblack/image-information](https://packagist.org/packages/bitandblack/image-information#3.3.0) | 3.3.0 | 4,468 | SVG dimension reader only; PECL Imagick 3.8.1 parses via ImageMagick delegate. | ImageMagick SVG reader via PECL Imagick |
| 11 | [mober/phpsvg](https://packagist.org/packages/mober/phpsvg#v6.0.0) | v6.0.0 | 2,972 | Typed SVG document wrapper over SimpleXML with two rectangle nodes observed. | mober phpsvg SimpleXML SVG document parser |
| 12 | [itools/svgsecuritycheck](https://packagist.org/packages/itools/svgsecuritycheck#v1.0.0) | v1.0.0 | 2,783 | Format-aware SVG validation verdict on one valid two-rectangle document; no element tree returned. | SvgSecurityCheck XMLReader-based SVG validator |
| 13 | [laratusk/larasvg](https://packagist.org/packages/laratusk/larasvg#v2.5.1) | v2.5.1 | 1,980 | Public converter class with isolated Illuminate Process facade factory; librsvg 2.63.4 renders the SVG. | GNOME librsvg SVG renderer via rsvg-convert |
| 14 | [atelier/svg](https://packagist.org/packages/atelier/svg#v1.1.0) | v1.1.0 | 1,077 | Typed SVG document and two parsed rectangles. | Atelier SVG typed DOM parser |
| 15 | [atelier/rasterizer](https://packagist.org/packages/atelier/rasterizer#v0.7.0) | v0.7.0 | 151 | Rendered two-rectangle SVG to a 2 × 1 PNG using external librsvg 2.63.4. | GNOME librsvg SVG renderer via rsvg-convert |
| 16 | [mgrulich/php-svg-lib](https://packagist.org/packages/mgrulich/php-svg-lib#v0.5) | v0.5 | 24 | SVG root width and height only; full rendering not exercised. | dompdf php-svg-lib XML/SVG parser |
| 17 | [yoya/php-svg](https://packagist.org/packages/yoya/php-svg#v1.0.0) | v1.0.0 | 19 | Typed SVG root dimensions and two parsed rectangle child nodes. | mediashowroom PHP-SVG typed document parser |
| 18 | [renfordt/php-svg](https://packagist.org/packages/renfordt/php-svg#v0.1.0) | v0.1.0 | 13 | Typed SVG root dimensions and two rectangle nodes. | meyfa PHP-SVG typed document parser |
| 19 | [phil/svg-sanitizer](https://packagist.org/packages/phil/svg-sanitizer#0.1.0-alpha) | 0.1.0-alpha | 11 | Valid two-rectangle SVG reconstructed through SVG element/attribute allowlists. | PHIL SVG sanitizer over PHP Dom XMLDocument |
| 20 | [decmuc/svgsanitizer](https://packagist.org/packages/decmuc/svgsanitizer#v1.1.1) | v1.1.1 | 10 | Valid SVG accepted and reconstructed with two rectangle nodes; no security assessment made. | decMuc SVG sanitizer over libxml DOM |

The two verified [PHP 8.5 runtime APIs](standard.json) are separate from this ranking. Several package paths share the same enshrined sanitizer, PHP-SVG lineage, dompdf parser, or librsvg engine. The two exact-source Packagist aliases in [leads.json](leads.json) are excluded.
