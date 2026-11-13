#include <SDL_sound.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  if (!Sound_Init()) return 1;
  Sound_Sample *sample = Sound_NewSampleFromFile(argv[1], NULL, 4096);
  if (!sample) { Sound_Quit(); return 1; }
  unsigned decoded_bytes = Sound_Decode(sample);
  int duration_ms = Sound_GetDuration(sample);
  if (decoded_bytes == 0 || duration_ms <= 0) {
    Sound_FreeSample(sample);
    Sound_Quit();
    return 1;
  }
  printf("{\"sample_rate\":%u,\"channels\":%u,\"decoded_bytes\":%u,\"duration_ms\":%d}\n",
         sample->actual.rate, sample->actual.channels, decoded_bytes, duration_ms);
  Sound_FreeSample(sample);
  Sound_Quit();
  return 0;
}
