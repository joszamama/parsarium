#include "harness.h"
#include <AL/alut.h>
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
    int ok = 0;
    if (alutInit(NULL, NULL)) {
        ALenum format = 0;
        ALsizei length = 0;
        ALfloat frequency = 0;
        ALvoid *pcm = alutLoadMemoryFromFile(path, &format, &length, &frequency);
        if (pcm && format == AL_FORMAT_MONO16 && length >= 8 && frequency > 0) {
            result->sample_rate = (unsigned)frequency;
            result->channels = 1;
            result->frames = (uint64_t)length / 2;
            memcpy(result->samples, pcm, 8);
            ok = 1;
        }
        free(pcm);
        alutExit();
    }
    unlink(path);
    return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    Result result;
    (void)parse_data(data, size, &result);
    return 0;
}
