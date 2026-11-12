#include <SDL.h>
#include <stdint.h>
#include <string.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    SDL_AudioSpec spec;
    Uint8 *bytes = NULL;
    Uint32 length = 0;
    if (!SDL_LoadWAV(argv[1], &spec, &bytes, &length)) return 3;
    if (spec.freq != 8000 || spec.channels != 1 ||
        spec.format != AUDIO_S16LSB || length < 8) return 4;
    int16_t samples[4];
    memcpy(samples, bytes, sizeof(samples));
    wav_report((unsigned int)spec.freq, (unsigned int)spec.channels,
               length / (2 * spec.channels), samples);
    SDL_FreeWAV(bytes);
    return 0;
}
