#include <SDL.h>
#include <SDL_mixer.h>
#include <stdint.h>
#include <string.h>

#include "report.h"

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    SDL_setenv("SDL_AUDIODRIVER", "dummy", 1);
    if (SDL_Init(SDL_INIT_AUDIO) != 0 ||
        Mix_OpenAudio(8000, AUDIO_S16SYS, 1, 2048) != 0) return 3;
    Mix_Chunk *chunk = Mix_LoadWAV(argv[1]);
    if (!chunk || chunk->alen < 8) return 4;
    int frequency = 0, channels = 0;
    Uint16 format = 0;
    if (!Mix_QuerySpec(&frequency, &format, &channels) ||
        frequency != 8000 || channels != 1 || format != AUDIO_S16SYS) return 5;
    int16_t samples[4];
    memcpy(samples, chunk->abuf, sizeof(samples));
    wav_report((unsigned int)frequency, (unsigned int)channels,
               chunk->alen / (2 * channels), samples);
    Mix_FreeChunk(chunk);
    Mix_CloseAudio();
    SDL_Quit();
    return 0;
}
