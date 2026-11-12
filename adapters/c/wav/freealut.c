#include <AL/alut.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!alutInit(NULL, NULL)) return 3;
    ALenum format = 0;
    ALsizei size = 0;
    ALfloat frequency = 0;
    ALvoid *buffer = alutLoadMemoryFromFile(argv[1], &format, &size, &frequency);
    if (!buffer || format != AL_FORMAT_MONO16 || size < 8) {
        fprintf(stderr, "freealut: buffer=%p format=%d size=%d rate=%.0f error=%s\n",
                buffer, format, size, frequency, alutGetErrorString(alutGetError()));
        return 4;
    }
    int16_t samples[4];
    memcpy(samples, buffer, sizeof(samples));
    wav_report((unsigned int)frequency, 1, (uint64_t)size / 2, samples);
    free(buffer);
    alutExit();
    return 0;
}
