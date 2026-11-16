#define _GNU_SOURCE
#include "harness.h"
#include <imago2.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parsarium_parse_pnm(const uint8_t *data, size_t size, struct parsarium_pnm_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  char path[] = "/tmp/parsarium-imago-XXXXXX.ppm";
  int fd = mkstemps(path, 4);
  if (fd < 0) return 0;
  size_t written = 0;
  while (written < size) {
    ssize_t n = write(fd, data + written, size - written);
    if (n <= 0) { close(fd); unlink(path); return 0; }
    written += (size_t)n;
  }
  close(fd);
  struct img_pixmap image;
  img_init(&image);
  int loaded = img_load(&image, path);
  unlink(path);
  if (loaded != 0 || image.width < 2 || image.height < 1 ||
      img_set_format(&image, IMG_FMT_RGBA32) != 0) {
    img_destroy(&image);
    return 0;
  }
  unsigned char *pixels = image.pixels;
  result->width = image.width; result->height = image.height;
  for (int c = 0; c < 4; ++c) {
    result->first[c] = pixels[c];
    result->second[c] = pixels[4 + c];
  }
  img_destroy(&image);
  return 1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_pnm_result result;
  (void)parsarium_parse_pnm(data, size, &result);
  return 0;
}
