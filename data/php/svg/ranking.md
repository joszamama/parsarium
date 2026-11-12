# PHP × SVG: verified parser ranking

Five verified third-party source paths, below the working goal of 20 and original ceiling of 30. The metric is Packagist lifetime downloads saved with eight bounded search queries on 2026-11-12. It covers all uses of each package and only compares adoption within PHP. Five named leads remain unresolved; this is not a definitive most-used top five or top twenty.

| Rank | Package | Pinned release | Lifetime downloads | Observable SVG result | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [dompdf/php-svg-lib](https://packagist.org/packages/dompdf/php-svg-lib#1.0.2) | 1.0.2 | 80,006,827 | Root dimensions 2 × 1 | dompdf php-svg-lib XML/SVG parser |
| 2 | [enshrined/svg-sanitize](https://packagist.org/packages/enshrined/svg-sanitize#1.1.1) | 1.1.1 | 55,204,366 | Two retained rectangle elements and first fill | enshrined SVG sanitizer over libxml DOM |
| 3 | [meyfa/php-svg](https://packagist.org/packages/meyfa/php-svg#v0.16.1) | v0.16.1 | 19,147,610 | Typed SVG tree with two rectangles | meyfa PHP-SVG typed document parser |
| 4 | [mathiasreker/php-svg-optimizer](https://packagist.org/packages/mathiasreker/php-svg-optimizer#10.0.0) | 10.0.0 | 25,661 | First rectangle fill normalized from `#ff0000` to `red` | MathiasReker SVG optimizer over libxml DOM |
| 5 | [atelier/svg](https://packagist.org/packages/atelier/svg#v1.1.0) | v1.1.0 | 1,077 | Typed SVG tree with two rectangles | Atelier SVG typed DOM parser |

The separate [PHP runtime inventory](standard.json) verifies `getimagesize()` and `getimagesizefromstring()` on this control in PHP 8.5. Both expose the same bundled SVG dimension parser through different input APIs; they are excluded from this third-party ranking. `phenx/php-svg-lib` and `jangobrick/php-svg` resolve to source releases already counted above and are excluded as aliases.
