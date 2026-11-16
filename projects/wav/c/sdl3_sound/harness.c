#include "harness.h"
#include <SDL3/SDL.h>
#include <SDL3_sound/SDL_sound.h>
#include <string.h>

int parsarium_parse_wav(const uint8_t *data, size_t size, struct parsarium_wav_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  if (!Sound_Init()) return 0;
  Sound_Sample *sample = Sound_NewSampleFromMem(data, (Uint32)size, "wav", NULL, 4096);
  if (!sample) { Sound_Quit(); return 0; }
  Uint32 length = Sound_DecodeAll(sample);
  int ok = sample->actual.freq == 8000 && sample->actual.channels == 1 &&
           sample->actual.format == SDL_AUDIO_S16LE && length == 8;
  if (ok) {
    result->sample_rate = sample->actual.freq;
    result->channels = sample->actual.channels;
    result->frames = length / (2u * sample->actual.channels);
    memcpy(result->samples, sample->buffer, sizeof(result->samples));
  }
  Sound_FreeSample(sample); Sound_Quit();
  return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_wav_result result;
  (void)parsarium_parse_wav(data, size, &result);
  return 0;
}
