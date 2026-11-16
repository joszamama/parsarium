#include "harness.h"
#include <jasper/jasper.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int parsarium_parse_pnm(const uint8_t *data, size_t size,
                       struct parsarium_pnm_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    *result = (struct parsarium_pnm_result){0};
    static int initialized;
    if (!initialized) {
        if (jas_init() != 0) return 0;
        initialized = 1;
    }
    char path[] = "/tmp/parsarium-jasper-XXXXXX.ppm";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t written = 0;
    while (written < size) {
        ssize_t count = write(fd, data + written, size - written);
        if (count <= 0) { close(fd); unlink(path); return 0; }
        written += (size_t)count;
    }
    close(fd);
    jas_stream_t *stream = jas_stream_fopen(path, "rb");
    unlink(path);
    if (!stream) return 0;
    jas_image_t *image = jas_image_decode(stream, -1, NULL);
    if (!image) { jas_stream_close(stream); return 0; }
    int okay = 0;
    if (jas_image_numcmpts(image) == 3 &&
        jas_image_width(image) >= 2 && jas_image_height(image) >= 1) {
        result->width = jas_image_width(image);
        result->height = jas_image_height(image);
        okay = 1;
        for (unsigned channel = 0; channel < 3; ++channel) {
            int first = jas_image_readcmptsample(image, channel, 0, 0);
            int second = jas_image_readcmptsample(image, channel, 1, 0);
            if (first < 0 || second < 0) { okay = 0; break; }
            result->first[channel] = first;
            result->second[channel] = second;
        }
    }
    jas_image_destroy(image);
    jas_stream_close(stream);
    return okay;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_pnm_result result;
    (void)parsarium_parse_pnm(data, size, &result);
    return 0;
}
