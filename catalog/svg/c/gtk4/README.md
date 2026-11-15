# gtk4 — SVG / C

- **Pinned release:** `4.24.1`
- **License:** LGPL-2.1-or-later
- **Parsed scope:** SVG root dimensions parsed by GtkSvg from local file bytes
- **Underlying family:** GTK 4 native GtkSvg parser
- **Local input API:** `g_file_get_contents(local SVG filename); gtk_svg_new_from_bytes(GBytes); gdk_paintable_get_intrinsic_width/height`
- **Documentation:** [API reference](<https://docs.gtk.org/gtk4/ctor.Svg.new_from_bytes.html>)
- **Catalog evidence:** [parser record](../../../../data/c/svg/parsers.json) · [control verification](../../../../data/c/svg/verification.json) · [within-ecosystem ranking](../../../../data/c/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

GtkSvg is the GTK 4.22+ built-in parser under gtk/svg, separate from the librsvg-backed GdkPixbuf loader. This API reports parsed document dimensions; pixel rendering is not exercised.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
