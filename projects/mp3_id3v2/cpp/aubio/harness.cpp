#include "harness.h"
#include <aubio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.mp3";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    aubio_source_t *source = new_aubio_source(path, 0, 256);
    unlink(path);
    if (!source) return 0;
    fvec_t *samples = new_fvec(256);
    if (!samples) { del_aubio_source(source); return 0; }
    uint_t read = 0;
    aubio_source_do(source, samples, &read);
    int ok = read == 256;
    if (ok) {
        result->sample_rate = aubio_source_get_samplerate(source);
        result->channels = aubio_source_get_channels(source);
        result->decoded_samples = read;
    }
    del_fvec(samples);
    del_aubio_source(source);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_mp3_result result;
    (void)parsarium_parse_mp3(data, size, &result);
    return 0;
}
