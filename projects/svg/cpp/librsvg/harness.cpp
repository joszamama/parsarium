#include "harness.h"

#include <cairo.h>
#include <librsvg/rsvg.h>

#include <cmath>
#include <cstdio>
#include <cstring>
#include <memory>
#include <string>
#include <unistd.h>

#if __cplusplus < 201703L
#error "the librsvg C++ harness is a C++17 translation unit"
#endif

namespace {

// Rendering is bounded so a declared huge canvas cannot exhaust memory.
constexpr double kMaxPixels = 4096.0 * 4096.0;

struct HandleDeleter {
    void operator()(RsvgHandle *handle) const { g_object_unref(handle); }
};
struct SurfaceDeleter {
    void operator()(cairo_surface_t *surface) const { cairo_surface_destroy(surface); }
};
struct ContextDeleter {
    void operator()(cairo_t *cr) const { cairo_destroy(cr); }
};
using Handle = std::unique_ptr<RsvgHandle, HandleDeleter>;
using Surface = std::unique_ptr<cairo_surface_t, SurfaceDeleter>;
using Context = std::unique_ptr<cairo_t, ContextDeleter>;

// Owns a GError out-parameter; librsvg reports failures through it.
class ErrorSlot {
public:
    ErrorSlot() = default;
    ErrorSlot(const ErrorSlot &) = delete;
    ErrorSlot &operator=(const ErrorSlot &) = delete;
    ~ErrorSlot() { g_clear_error(&error_); }
    GError **out() { return &error_; }

private:
    GError *error_ = nullptr;
};

// The documented API takes a filename, so the bytes go to a private directory.
// librsvg only resolves relative references below the file's own directory.
// The destructor removes both the file and the directory.
class PrivateInput {
public:
    PrivateInput(const std::uint8_t *data, std::size_t size) {
        char dir[] = "/tmp/parsarium-librsvg-cpp-XXXXXX";
        if (!mkdtemp(dir)) return;
        dir_ = dir;
        path_ = dir_ + "/input.svg";
        std::FILE *file = std::fopen(path_.c_str(), "wb");
        bool written = file && std::fwrite(data, 1, size, file) == size;
        if (file && std::fclose(file) != 0) written = false;
        ok_ = written;
    }
    PrivateInput(const PrivateInput &) = delete;
    PrivateInput &operator=(const PrivateInput &) = delete;
    ~PrivateInput() {
        if (dir_.empty()) return;
        unlink(path_.c_str());
        rmdir(dir_.c_str());
    }
    bool ok() const { return ok_; }
    const char *path() const { return path_.c_str(); }

private:
    std::string dir_;
    std::string path_;
    bool ok_ = false;
};

// Cairo ARGB32 is native-endian premultiplied; report straight RGB.
void copy_rgb(unsigned char output[3], const unsigned char *pixel) {
    std::uint32_t argb;
    std::memcpy(&argb, pixel, sizeof(argb));
    const unsigned alpha = argb >> 24;
    for (int i = 0; i < 3; ++i) {
        const unsigned value = (argb >> (16 - 8 * i)) & 255;
        output[i] = alpha ? static_cast<unsigned char>((value * 255 + alpha / 2) / alpha) : 0;
    }
}

bool render(RsvgHandle *handle, parsarium_svg_result *result) {
    double width = 0, height = 0;
    if (!rsvg_handle_get_intrinsic_size_in_pixels(handle, &width, &height)) return false;
    if (!std::isfinite(width) || !std::isfinite(height) || width <= 0 || height <= 0 ||
        width > kMaxPixels || height > kMaxPixels)
        return false;
    const double surface_width = std::ceil(width), surface_height = std::ceil(height);
    if (surface_width * surface_height > kMaxPixels) return false;
    const int w = static_cast<int>(surface_width), h = static_cast<int>(surface_height);
    Surface surface(cairo_image_surface_create(CAIRO_FORMAT_ARGB32, w, h));
    if (cairo_surface_status(surface.get()) != CAIRO_STATUS_SUCCESS) return false;
    {
        Context cr(cairo_create(surface.get()));
        const RsvgRectangle viewport = {0, 0, width, height};
        ErrorSlot error;
        if (!rsvg_handle_render_document(handle, cr.get(), &viewport, error.out()) ||
            cairo_status(cr.get()) != CAIRO_STATUS_SUCCESS)
            return false;
    }
    cairo_surface_flush(surface.get());
    const unsigned char *pixels = cairo_image_surface_get_data(surface.get());
    const int stride = cairo_image_surface_get_stride(surface.get());
    if (!pixels) return false;
    result->width = static_cast<unsigned>(w);
    result->height = static_cast<unsigned>(h);
    copy_rgb(result->first, pixels);
    result->second_present = static_cast<long>(w) * h > 1;
    if (result->second_present)
        copy_rgb(result->second, w > 1 ? pixels + 4 : pixels + stride);
    return true;
}

}  // namespace

bool parsarium_parse_svg(const std::uint8_t *data, std::size_t size,
                         parsarium_svg_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return false;
    *result = parsarium_svg_result{};
    PrivateInput input(data, size);
    if (!input.ok()) return false;
    ErrorSlot error;
    Handle handle(rsvg_handle_new_from_file(input.path(), error.out()));
    return handle && render(handle.get(), result);
}
