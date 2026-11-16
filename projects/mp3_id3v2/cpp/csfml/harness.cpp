#include "harness.h"
#include <CSFML/Audio/SoundBuffer.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parse_data(const uint8_t *data, size_t size, Result *result) {
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
    int ok = 0;
    sfSoundBuffer *buffer = sfSoundBuffer_createFromFile(path);
    if (buffer) {
        const int16_t *pcm = sfSoundBuffer_getSamples(buffer);
        result->samples = sfSoundBuffer_getSampleCount(buffer);
        result->sample_rate = sfSoundBuffer_getSampleRate(buffer);
        result->channels = sfSoundBuffer_getChannelCount(buffer);
        ok = pcm && result->samples > 0 && result->sample_rate > 0 && result->channels > 0;
        sfSoundBuffer_destroy(buffer);
    }
    unlink(path);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
