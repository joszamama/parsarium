#include <CSFML/Audio/SoundBuffer.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  sfSoundBuffer *buffer = sfSoundBuffer_createFromFile(argv[1]);
  if (!buffer) return 1;
  uint64_t samples = sfSoundBuffer_getSampleCount(buffer);
  unsigned int rate = sfSoundBuffer_getSampleRate(buffer);
  unsigned int channels = sfSoundBuffer_getChannelCount(buffer);
  if (!sfSoundBuffer_getSamples(buffer) || samples == 0) return 1;
  printf("{\"samples\":%llu,\"sample_rate\":%u,\"channels\":%u}\n",
         (unsigned long long)samples, rate, channels);
  sfSoundBuffer_destroy(buffer);
  return 0;
}
