#include "harness.h"
#include <raylib.h>
#include <stdio.h>
#include <string.h>

int parsarium_parse_wav(const uint8_t *data, size_t size, struct parsarium_wav_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  SetTraceLogLevel(LOG_NONE);
  Wave wave = LoadWaveFromMemory(".wav", data, (int)size);
  if (!wave.data) {
    snprintf(result->error, sizeof(result->error), "LoadWaveFromMemory returned no data");
    return 0;
  }
  result->sample_rate = wave.sampleRate;
  result->channels = wave.channels;
  result->frames = wave.frameCount;
  /* raylib decodes WAV to 16-bit samples (sampleSize 16); report the first four. */
  unsigned long long count = wave.sampleSize == 16 ? (unsigned long long)wave.frameCount * wave.channels : 0;
  result->sample_count = (unsigned)(count < 4 ? count : 4);
  memcpy(result->samples, wave.data, result->sample_count * sizeof(int16_t));
  UnloadWave(wave);
  return 1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_wav_result result;
  (void)parsarium_parse_wav(data, size, &result);
  return 0;
}
