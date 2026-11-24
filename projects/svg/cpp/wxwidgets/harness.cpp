#include "harness.h"

#include <wx/bmpbndl.h>
#include <wx/image.h>
#include <wx/init.h>
#include <wx/log.h>

#include <algorithm>
#include <cstdlib>
#include <unistd.h>

#if !defined(wxHAS_SVG) || !wxUSE_NANOSVG || wxUSE_NANOSVG_EXTERNAL || wxUSE_LUNASVG
#error "wxWidgets must be built with its bundled NanoSVG backend"
#endif

bool parsarium_parse_svg(const std::uint8_t *data, std::size_t size,
                         parsarium_svg_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return false;
    static wxInitializer initializer;
    static bool configured = false;
    if (!initializer.IsOk()) return false;
    if (!configured) {
        // Debug-build asserts would otherwise open a dialog under Xvfb.
        wxSetAssertHandler(nullptr);
        configured = true;
    }

    char path[] = "/tmp/parsarium-wx-svg-XXXXXX.svg";
    int fd = mkstemps(path, 4);
    if (fd < 0) return false;
    bool written = true;
    for (std::size_t offset = 0; offset < size;) {
        ssize_t count = write(fd, data + offset, size - offset);
        if (count <= 0) { written = false; break; }
        offset += static_cast<std::size_t>(count);
    }
    if (close(fd) != 0) written = false;
    if (!written) { unlink(path); return false; }

    wxLogNull quiet;
    // wxDefaultSize makes the bundle use the SVG's own width and height.
    wxBitmapBundle bundle = wxBitmapBundle::FromSVGFile(wxString::FromUTF8(path),
                                                        wxDefaultSize);
    unlink(path);
    if (!bundle.IsOk()) return false;
    wxSize svg_size = bundle.GetDefaultSize();
    if (svg_size.x <= 0 || svg_size.y <= 0) return false;
    // Render at the SVG's own size, as wxDefaultSize selects.
    wxImage image = bundle.GetBitmap(svg_size).ConvertToImage();
    if (!image.IsOk() || !image.GetData()) return false;
    int width = image.GetWidth();
    int height = image.GetHeight();
    if (width <= 0 || height <= 0) return false;
    const unsigned char *rgb = image.GetData();
    result->width = width;
    result->height = height;
    for (int i = 0; i < 3; ++i) result->first[i] = rgb[i];
    result->second_present = static_cast<std::size_t>(width) * height > 1;
    if (result->second_present)
        for (int i = 0; i < 3; ++i) result->second[i] = rgb[3 + i];
    return true;
}
