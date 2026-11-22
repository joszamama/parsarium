#include "harness.h"
#include <aubio.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

int parsarium_parse_wav(const uint8_t *data, size_t size, struct parsarium_wav_result *result) {
    if (!data || !result || !size || size > (1u << 20)) return 0;
    memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.wav";
    int fd = mkstemps(path, 4);
    if (fd < 0) return 0;
    size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return 0; }
        offset += (size_t)n;
    }
    close(fd);
    aubio_source_t *source = new_aubio_source(path, 0, 4);
    unlink(path);
    if (!source) {
        snprintf(result->error, sizeof(result->error), "new_aubio_source failed");
        return 0;
    }
    uint_t channels = aubio_source_get_channels(source);
    result->sample_rate = aubio_source_get_samplerate(source);
    result->channels = channels;
    result->frames = aubio_source_get_duration(source);
    /* One hop of four frames per channel; the first four interleaved samples. */
    fmat_t *samples = channels ? new_fmat(channels, 4) : NULL;
    if (samples) {
        uint_t read = 0;
        aubio_source_do_multi(source, samples, &read);
        unsigned count = 0;
        for (uint_t frame = 0; frame < read && count < 4; frame++)
            for (uint_t channel = 0; channel < channels && count < 4; channel++) {
                float x = samples->data[channel][frame] * 32768.0f;
                result->samples[count++] = (int16_t)(x >= 32767.0f ? 32767 : x <= -32768.0f ? -32768 : lroundf(x));
            }
        result->sample_count = count;
        del_fmat(samples);
    }
    del_aubio_source(source);
    return 1;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    struct parsarium_wav_result result;
    (void)parsarium_parse_wav(data, size, &result);
    return 0;
}
