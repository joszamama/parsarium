#define _GNU_SOURCE
#include "harness.h"
#include <sail/sail.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int parsarium_parse_pnm(const uint8_t *data, size_t size, struct parsarium_pnm_result *result) {
 if (!data || !result || size == 0 || size > (1u << 20)) return 0;
 memset(result, 0, sizeof(*result));
 char path[] = "/tmp/parsarium-sail-XXXXXX.ppm";
 int fd = mkstemps(path, 4);
 if (fd < 0) return 0;
 size_t offset = 0;
 while (offset < size) {
  ssize_t count = write(fd, data + offset, size - offset);
  if (count <= 0) { close(fd); unlink(path); return 0; }
  offset += (size_t)count;
 }
 close(fd);
 struct sail_image *image = NULL;
 sail_status_t status = sail_load_from_file(path, &image);
 unlink(path);
 if (status != SAIL_OK || !image) { if (image) sail_destroy_image(image); return 0; }
 if (image->pixel_format != SAIL_PIXEL_FORMAT_BPP24_RGB ||
     image->width < 2 || image->height < 1 || image->bytes_per_line < 6) {
  sail_destroy_image(image); return 0;
 }
 const unsigned char *pixels = image->pixels;
 result->width = (int)image->width; result->height = (int)image->height;
 for (int i = 0; i < 3; i++) { result->first[i] = pixels[i]; result->second[i] = pixels[i+3]; }
 sail_destroy_image(image);
 return 1;
}
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
 struct parsarium_pnm_result result;
 (void)parsarium_parse_pnm(data, size, &result);
 return 0;
}
