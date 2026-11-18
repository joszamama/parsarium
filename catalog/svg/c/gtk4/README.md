# gtk4 — SVG / C

- **Pinned release:** `4.24.1`
- **Upstream:** [source repository](<https://gitlab.gnome.org/GNOME/gtk>) · [Debian](<https://tracker.debian.org/pkg/gtk4>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/c/gtk4/README.md)

```sh
python3 parsarium.py build svg c gtk4
python3 parsarium.py run svg c gtk4 controls/svg/red-green.svg
```
