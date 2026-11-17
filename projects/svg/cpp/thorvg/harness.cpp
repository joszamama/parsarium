#include "harness.h"
#include <cmath>
#include <cstring>
#include <memory>
#include <thorvg.h>
#include <unistd.h>
#include <vector>

static constexpr float kMaxSide = 4096.0f;

// Adapter path: tvg::Picture::load(local filename) followed by Picture::size.
// Bytes are written to a fresh .svg file so ThorVG's own file loader reads them.
int parsarium_parse_svg(const uint8_t *data, size_t size, struct parsarium_svg_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    std::memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-thorvg-XXXXXX.svg";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    if (tvg::Initializer::init(0) != tvg::Result::Success) { unlink(path); return 0; }
    int ok = 0;
    {
        tvg::Picture *picture = tvg::Picture::gen();
        float fw = 0, fh = 0;
        bool loaded = picture && picture->load(path) == tvg::Result::Success;
        unlink(path); // the SVG loader has copied the file contents by now
        if (loaded && picture->size(&fw, &fh) == tvg::Result::Success && std::isfinite(fw) && std::isfinite(fh) &&
            fw > 0.0f && fh > 0.0f && fw <= kMaxSide && fh <= kMaxSide) {
            unsigned w = (unsigned)std::lround(fw), h = (unsigned)std::lround(fh);
            if (!w) w = 1;
            if (!h) h = 1;
            std::vector<uint32_t> pixels((size_t)w * h);
            std::unique_ptr<tvg::SwCanvas> canvas(tvg::SwCanvas::gen());
            if (canvas &&
                canvas->target(pixels.data(), w, w, h, tvg::ColorSpace::ARGB8888S) == tvg::Result::Success &&
                canvas->add(picture) == tvg::Result::Success) {
                picture = nullptr; // owned by the canvas
                if (canvas->draw(true) == tvg::Result::Success && canvas->sync() == tvg::Result::Success) {
                    result->width = w;
                    result->height = h;
                    ok = 1;
                }
            }
        }
        if (picture) tvg::Paint::rel(picture);
    }
    tvg::Initializer::term();
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_svg_result result;
    (void)parsarium_parse_svg(data, size, &result);
    return 0;
}
