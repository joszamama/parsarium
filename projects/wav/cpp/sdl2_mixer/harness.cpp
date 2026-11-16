#include "harness.h"
#include <SDL.h>
#include <SDL_mixer.h>
#include <string.h>

int parsarium_parse_wav(const uint8_t *data, size_t size, struct parsarium_wav_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  SDL_setenv("SDL_AUDIODRIVER", "dummy", 1);
  if (SDL_Init(SDL_INIT_AUDIO) != 0) return 0;
  if (Mix_OpenAudio(8000, AUDIO_S16LSB, 1, 2048) != 0) { SDL_Quit(); return 0; }
  SDL_RWops *input = SDL_RWFromConstMem(data, (int)size);
  if (!input) { Mix_CloseAudio(); SDL_Quit(); return 0; }
  Mix_Chunk *chunk = Mix_LoadWAV_RW(input, 1);
  if (!chunk) { Mix_CloseAudio(); SDL_Quit(); return 0; }
  int frequency=0, channels=0; Uint16 format=0;
  int ok = Mix_QuerySpec(&frequency,&format,&channels) && frequency==8000 && channels==1 &&
           format==AUDIO_S16LSB && chunk->alen==8;
  if (ok) {
    result->sample_rate=frequency; result->channels=channels; result->frames=chunk->alen/(2u*channels);
    memcpy(result->samples,chunk->abuf,sizeof(result->samples));
  }
  Mix_FreeChunk(chunk); Mix_CloseAudio(); SDL_Quit();
  return ok;
}
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data,size_t size) {
  struct parsarium_wav_result result;
  (void)parsarium_parse_wav(data,size,&result);
  return 0;
}
