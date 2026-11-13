#include <lame.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  FILE *file = fopen(argv[1], "rb");
  if (!file) return 1;
  if (fseek(file, 0, SEEK_END) != 0) return 1;
  long length = ftell(file);
  if (length <= 0 || length > 1000000) return 1;
  rewind(file);
  unsigned char *bytes = (unsigned char *)malloc((size_t)length);
  if (!bytes) return 1;
  if (fread(bytes, 1, (size_t)length, file) != (size_t)length) return 1;
  fclose(file);
  hip_t decoder = hip_decode_init();
  if (!decoder) return 1;
  short left[1152], right[1152];
  mp3data_struct frame;
  memset(&frame, 0, sizeof(frame));
  int decoded = hip_decode1_headers(decoder, bytes, (size_t)length,
                                    left, right, &frame);
  if (decoded <= 0 || !frame.header_parsed) return 1;
  printf("{\"sample_rate\":%d,\"channels\":%d,\"bitrate_kbps\":%d,\"decoded_samples\":%d}\n",
         frame.samplerate, frame.stereo, frame.bitrate, decoded);
  hip_decode_exit(decoder);
  free(bytes);
  return 0;
}
