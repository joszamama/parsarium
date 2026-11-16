#include "harness.h"
#include <SDL.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parse_data(const uint8_t *data, size_t size, Result *result) {
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
    SDL_AudioSpec spec;
    Uint8 *pcm = NULL;
    Uint32 length = 0;
    int ok = 0;
    if (SDL_LoadWAV(path, &spec, &pcm, &length)) {
        if (spec.freq > 0 && spec.channels > 0 && spec.format == AUDIO_S16LSB && length >= 8) {
            result->sample_rate = (unsigned)spec.freq;
            result->channels = (unsigned)spec.channels;
            result->frames = length / (2u * spec.channels);
            memcpy(result->samples, pcm, 8);
            ok = 1;
        }
        SDL_FreeWAV(pcm);
    }
    unlink(path);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
