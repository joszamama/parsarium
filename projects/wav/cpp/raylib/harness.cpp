#include "harness.h"
#include <raylib.h>
#include <string.h>

int parsarium_parse_wav(const uint8_t *data, size_t size, struct parsarium_wav_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  SetTraceLogLevel(LOG_NONE);
  Wave wave = LoadWaveFromMemory(".wav", data, (int)size);
  if (!wave.data) return 0;
  int ok = wave.channels == 1 && wave.sampleRate == 8000 &&
           wave.sampleSize == 16 && wave.frameCount >= 4;
  if (ok) {
    const int16_t *pcm = (const int16_t *)wave.data;
    result->sample_rate = wave.sampleRate;
    result->channels = wave.channels;
    result->frames = wave.frameCount;
    memcpy(result->samples, pcm, sizeof(result->samples));
  }
  UnloadWave(wave);
  return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_wav_result result;
  (void)parsarium_parse_wav(data, size, &result);
  return 0;
}
