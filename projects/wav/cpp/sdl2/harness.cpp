#include "harness.h"
#include <SDL.h>
#include <string.h>

int parsarium_parse_wav(const uint8_t *data, size_t size, struct parsarium_wav_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  if (SDL_Init(0) != 0) return 0;
  SDL_RWops *input = SDL_RWFromConstMem(data, (int)size);
  if (!input) { SDL_Quit(); return 0; }
  SDL_AudioSpec spec = {};
  Uint8 *pcm = NULL; Uint32 length = 0;
  if (!SDL_LoadWAV_RW(input, 1, &spec, &pcm, &length)) { SDL_Quit(); return 0; }
  int ok = spec.freq == 8000 && spec.channels == 1 &&
           spec.format == AUDIO_S16LSB && length >= 8;
  if (ok) {
    result->sample_rate = (unsigned)spec.freq;
    result->channels = (unsigned)spec.channels;
    result->frames = length / (2u * spec.channels);
    memcpy(result->samples, pcm, sizeof(result->samples));
  }
  SDL_FreeWAV(pcm); SDL_Quit();
  return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_wav_result result;
  (void)parsarium_parse_wav(data, size, &result);
  return 0;
}
