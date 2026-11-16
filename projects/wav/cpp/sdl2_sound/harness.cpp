#include "harness.h"
#include <SDL.h>
#include <SDL_sound.h>
#include <string.h>

int parsarium_parse_wav(const uint8_t *data, size_t size, struct parsarium_wav_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  if (!Sound_Init()) return 0;
  Sound_Sample *sample = Sound_NewSampleFromMem(data, (Uint32)size, "wav", NULL, 4096);
  if (!sample) { Sound_Quit(); return 0; }
  Uint32 length = Sound_DecodeAll(sample);
  int ok = sample->actual.rate == 8000 && sample->actual.channels == 1 &&
           sample->actual.format == AUDIO_S16LSB && length == 8;
  if (ok) {
    result->sample_rate = sample->actual.rate;
    result->channels = sample->actual.channels;
    result->frames = length / (2u * sample->actual.channels);
    memcpy(result->samples, sample->buffer, sizeof(result->samples));
  }
  Sound_FreeSample(sample); Sound_Quit();
  return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_wav_result result;
  (void)parsarium_parse_wav(data, size, &result);
  return 0;
}
