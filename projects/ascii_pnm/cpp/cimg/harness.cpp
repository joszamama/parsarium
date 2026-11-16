#define cimg_display 0
#include "harness.h"
#include <CImg.h>
#include <unistd.h>
#include <cstdio>

bool parsarium_parse_pnm(const uint8_t *data, size_t size, struct parsarium_pnm_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return false;
  *result = {};
  char path[] = "/tmp/parsarium-cimg-XXXXXX";
  int fd = mkstemp(path);
  if (fd < 0) return false;
  size_t written = 0;
  while (written < size) {
    ssize_t n = write(fd, data + written, size - written);
    if (n <= 0) { close(fd); unlink(path); return false; }
    written += static_cast<size_t>(n);
  }
  close(fd);
  try {
    auto image = cimg_library::CImg<unsigned char>::get_load_pnm(path);
    unlink(path);
    if (image.width() < 2 || image.height() < 1 || image.spectrum() != 3) return false;
    result->width = image.width(); result->height = image.height();
    for (int c = 0; c < 3; ++c) {
      result->first[c] = image(0, 0, 0, c);
      result->second[c] = image(1, 0, 0, c);
    }
    result->first[3] = result->second[3] = 255;
    return true;
  } catch (const cimg_library::CImgException&) {
    unlink(path);
    return false;
  }
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_pnm_result result;
  (void)parsarium_parse_pnm(data, size, &result);
  return 0;
}
