#include "harness.h"

#include <wx/image.h>
#include <wx/imagpnm.h>
#include <wx/init.h>
#include <wx/log.h>

#include <cstdlib>
#include <unistd.h>

bool parsarium_parse_pnm(const std::uint8_t *data, std::size_t size,
                         parsarium_pnm_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return false;
    static wxInitializer initializer;
    static bool registered = false;
    if (!initializer.IsOk()) return false;
    if (!registered) {
        wxImage::AddHandler(new wxPNMHandler);
        registered = true;
    }

    char path[] = "/tmp/parsarium-wx-pnm-XXXXXX";
    int fd = mkstemp(path);
    if (fd < 0) return false;
    bool written = true;
    for (std::size_t offset = 0; offset < size;) {
        ssize_t count = write(fd, data + offset, size - offset);
        if (count <= 0) { written = false; break; }
        offset += static_cast<std::size_t>(count);
    }
    if (close(fd) != 0) written = false;
    if (!written) { unlink(path); return false; }

    wxImage image;
    wxLogNull quiet;
    bool loaded = image.LoadFile(wxString::FromUTF8(path), wxBITMAP_TYPE_PNM);
    unlink(path);
    if (!loaded || !image.IsOk() || !image.GetData()) return false;
    int width = image.GetWidth();
    int height = image.GetHeight();
    if (width <= 0 || height <= 0) return false;
    const unsigned char *rgb = image.GetData();
    const unsigned char *alpha = image.HasAlpha() ? image.GetAlpha() : nullptr;
    result->width = width;
    result->height = height;
    for (int i = 0; i < 3; ++i) result->first[i] = rgb[i];
    result->first[3] = alpha ? alpha[0] : 255;
    result->second_present = static_cast<std::size_t>(width) * height > 1;
    if (result->second_present) {
        for (int i = 0; i < 3; ++i) result->second[i] = rgb[3 + i];
        result->second[3] = alpha ? alpha[1] : 255;
    }
    return true;
}
