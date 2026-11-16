#include "harness.h"
#include <boost/gil.hpp>
#include <boost/gil/extension/io/pnm.hpp>
#include <cstdio>
#include <cstdlib>
#include <unistd.h>

bool parsarium_parse_pnm(const std::uint8_t *data, std::size_t size,
                         parsarium_pnm_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return false;
    *result = {};
    char path[] = "/tmp/parsarium-gil-XXXXXX.ppm";
    int fd = mkstemps(path, 4);
    if (fd < 0) return false;
    std::size_t written = 0;
    while (written < size) {
        ssize_t count = write(fd, data + written, size - written);
        if (count <= 0) { close(fd); unlink(path); return false; }
        written += static_cast<std::size_t>(count);
    }
    close(fd);
    try {
        boost::gil::rgb8_image_t image;
        boost::gil::read_image(path, image, boost::gil::pnm_tag());
        unlink(path);
        auto view = boost::gil::const_view(image);
        if (view.width() < 2 || view.height() < 1) return false;
        auto first = view(0, 0), second = view(1, 0);
        result->width = static_cast<std::size_t>(view.width());
        result->height = static_cast<std::size_t>(view.height());
        result->first[0] = boost::gil::at_c<0>(first);
        result->first[1] = boost::gil::at_c<1>(first);
        result->first[2] = boost::gil::at_c<2>(first);
        result->first[3] = 255;
        result->second[0] = boost::gil::at_c<0>(second);
        result->second[1] = boost::gil::at_c<1>(second);
        result->second[2] = boost::gil::at_c<2>(second);
        result->second[3] = 255;
        return true;
    } catch (...) { unlink(path); return false; }
}

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    parsarium_pnm_result result;
    (void)parsarium_parse_pnm(data, size, &result);
    return 0;
}
