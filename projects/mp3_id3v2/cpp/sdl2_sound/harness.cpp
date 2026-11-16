#include "harness.h"
#include <SDL.h>
#include <SDL_sound.h>
#include <string.h>

int parsarium_parse_mp3(const uint8_t *data, size_t size, struct parsarium_mp3_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  if (!Sound_Init()) return 0;
  Sound_Sample *sample = Sound_NewSampleFromMem(data, (Uint32)size, "mp3", NULL, 4096);
  if (!sample) { Sound_Quit(); return 0; }
  Uint32 decoded = Sound_Decode(sample);
  int duration = Sound_GetDuration(sample);
  int ok = decoded != 0 && duration > 0;
  if (ok) {
    result->sample_rate = sample->actual.rate;
    result->channels = sample->actual.channels;
    result->decoded_bytes = decoded;
    result->duration_ms = duration;
  }
  Sound_FreeSample(sample); Sound_Quit();
  return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_mp3_result result;
  (void)parsarium_parse_mp3(data, size, &result);
  return 0;
}
