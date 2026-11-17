#include <sox.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  if (sox_init() != SOX_SUCCESS) return 1;
  sox_format_t *format = sox_open_read(argv[1], NULL, NULL, NULL);
  if (!format || !format->filetype || strcmp(format->filetype, "mp3") != 0) return 1;
  sox_sample_t sample = 0;
  size_t decoded = sox_read(format, &sample, 1);
  if (decoded != 1) return 1;
  printf("{\"filetype\":\"%s\",\"sample_rate\":%.0f,\"channels\":%u,\"decoded_samples\":%zu}\n",
         format->filetype, format->signal.rate, format->signal.channels, decoded);
  sox_close(format);
  sox_quit();
  return 0;
}
