#include "harness.h"
#include <OpenImageIO/imageio.h>
#include <cstring>
#include <string>
#include <vector>
#include <unistd.h>

int parsarium_parse_pnm(const uint8_t *data, size_t size, struct parsarium_pnm_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    std::memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.ppm";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += size_t(n);
    }
    close(fd);
    auto image = OIIO::ImageInput::open(path);
    if (!image || image->format_name() != std::string("pnm")) {
        unlink(path);
        return 0;
    }
    const OIIO::ImageSpec spec = image->spec();
    const bool ascii = spec.get_int_attribute("pnm:binary", -1) == 0;
    const bool dimensions = spec.width > 0 && spec.height > 0 &&
                            spec.width <= 4096 && spec.height <= 4096 &&
                            (spec.nchannels == 1 || spec.nchannels == 3);
    const size_t pixel_count = dimensions ? size_t(spec.width) * size_t(spec.height) : 0;
    const size_t channel_count = pixel_count * size_t(spec.nchannels);
    if (!ascii || !dimensions || channel_count > (1u << 24)) {
        image->close(); unlink(path); return 0;
    }
    std::vector<unsigned char> pixels(channel_count);
    bool read = image->read_image(0, 0, 0, spec.nchannels,
                                  OIIO::span<unsigned char>(pixels.data(), pixels.size()));
    image->close();
    unlink(path);
    if (!read) return 0;
    result->width = unsigned(spec.width);
    result->height = unsigned(spec.height);
    for (int channel = 0; channel < 3; ++channel) {
        int sample_channel = spec.nchannels == 1 ? 0 : channel;
        result->first[channel] = pixels[sample_channel];
        if (pixel_count > 1) result->second[channel] = pixels[spec.nchannels + sample_channel];
    }
    result->second_present = pixel_count > 1;
    return 1;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_pnm_result result;
    (void)parsarium_parse_pnm(data, size, &result);
    return 0;
}
