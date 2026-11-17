#include "harness.h"
#include <stdio.h>

static void print_codec(const char *name, const char *value) {
  printf(",\"%s\":", name);
  if (value[0]) printf("\"%s\"", value); else fputs("null", stdout);
}

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  FILE *file = fopen(argv[1], "rb");
  if (!file) return 3;
  static uint8_t input[1u << 20];
  size_t size = fread(input, 1, sizeof(input), file);
  if (ferror(file) || (size == sizeof(input) && fgetc(file) != EOF)) {
    fclose(file); return 4;
  }
  fclose(file);
  struct parsarium_mp4_result result;
  if (!parsarium_parse_mp4(input, size, &result)) return 5;
  printf("{\"video\":%d,\"audio\":%d,\"width\":%d,\"height\":%d",
         result.video, result.audio, result.width, result.height);
  print_codec("video_codec", result.video_codec);
  print_codec("audio_codec", result.audio_codec);
  puts("}");
  return 0;
}
