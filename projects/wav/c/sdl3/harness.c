#include "harness.h"
#include <SDL3/SDL.h>
#include <stdio.h>
#include <string.h>

/* One decoded sample as s16, for libraries that hand back their native
   sample format: unsigned integers are re-centred, wider integers keep their
   top 16 bits, floats are scaled by 32768, rounded and clamped. */
static int16_t parsarium_to_s16(const uint8_t *p, char kind, int bytes, int big_endian) {
    uint64_t raw = 0;
    for (int i = 0; i < bytes; i++)
        raw |= (uint64_t)p[big_endian ? i : bytes - 1 - i] << (8 * (bytes - 1 - i));
    if (kind == 'f') {
        double x;
        if (bytes == 4) { uint32_t bits = (uint32_t)raw; float f; memcpy(&f, &bits, 4); x = f; }
        else { double d; memcpy(&d, &raw, 8); x = d; }
        x = x * 32768.0;
        if (!(x > -32768.0)) return x != x ? 0 : -32768;
        if (x >= 32767.0) return 32767;
        return (int16_t)(x >= 0 ? x + 0.5 : x - 0.5); /* half away from zero */
    }
    if (kind == 'u') raw ^= (uint64_t)1 << (8 * bytes - 1);
    uint64_t top = bytes >= 2 ? raw >> (8 * bytes - 16) : raw << 8;
    return (int16_t)(uint16_t)(top & 0xFFFF);
}

int parsarium_parse_wav(const uint8_t *data, size_t size, struct parsarium_wav_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  if (!SDL_Init(0)) {
    snprintf(result->error, sizeof(result->error), "SDL_Init: %s", SDL_GetError());
    return 0;
  }
  SDL_IOStream *input = SDL_IOFromConstMem(data, size);
  if (!input) {
    snprintf(result->error, sizeof(result->error), "SDL_IOFromConstMem: %s", SDL_GetError());
    SDL_Quit(); return 0;
  }
  SDL_AudioSpec spec;
  memset(&spec, 0, sizeof(spec));
  Uint8 *pcm = NULL; Uint32 length = 0;
  if (!SDL_LoadWAV_IO(input, true, &spec, &pcm, &length)) {
    snprintf(result->error, sizeof(result->error), "SDL_LoadWAV_IO: %s", SDL_GetError());
    SDL_Quit(); return 0;
  }
  /* SDL returns the samples in the format it decoded them to (spec.format). */
  unsigned bytes = SDL_AUDIO_BYTESIZE(spec.format);
  char kind = SDL_AUDIO_ISFLOAT(spec.format) ? 'f' : SDL_AUDIO_ISSIGNED(spec.format) ? 's' : 'u';
  result->sample_rate = (unsigned)spec.freq;
  result->channels = (unsigned)spec.channels;
  result->frames = bytes && spec.channels ? length / (bytes * (unsigned)spec.channels) : 0;
  unsigned long long count = bytes ? length / bytes : 0;
  result->sample_count = (unsigned)(count < 4 ? count : 4);
  for (unsigned i = 0; i < result->sample_count; i++)
    result->samples[i] = parsarium_to_s16(pcm + i * bytes, kind, (int)bytes, SDL_AUDIO_ISBIGENDIAN(spec.format));
  SDL_free(pcm); SDL_Quit();
  return 1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_wav_result result;
  (void)parsarium_parse_wav(data, size, &result);
  return 0;
}
