#include <SDL3_sound/SDL_sound.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2 || !Sound_Init()) return 2;
    Sound_Sample *sample = Sound_NewSampleFromFile(argv[1], NULL, 4096);
    if (!sample) return 3;
    if (!sample->decoder || strcmp(sample->decoder->description, "Microsoft WAVE audio format") != 0) return 5;
    Uint32 bytes = Sound_DecodeAll(sample);
    if (sample->actual.format != SDL_AUDIO_S16LE || sample->actual.channels != 1 ||
        sample->desired.format != SDL_AUDIO_S16LE || bytes != 8) return 4;
    const uint8_t *p = (const uint8_t *) sample->buffer;
    int16_t values[4];
    for (int i = 0; i < 4; ++i) values[i] = (int16_t) ((uint16_t) p[2*i] | ((uint16_t) p[2*i+1] << 8));
    printf("{\"sample_rate\":%d,\"channels\":%u,\"frames\":%u,\"samples\":[%d,%d,%d,%d]}\n",
           sample->actual.freq, sample->actual.channels,
           bytes / (2 * sample->actual.channels), values[0], values[1], values[2], values[3]);
    Sound_FreeSample(sample);
    Sound_Quit();
    return 0;
}
