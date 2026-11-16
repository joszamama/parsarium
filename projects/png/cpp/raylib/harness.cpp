#include "harness.h"
#include <raylib.h>
#include <string.h>

int parsarium_parse_png(const uint8_t *data, size_t size, struct parsarium_png_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  SetTraceLogLevel(LOG_NONE);
  Image image = LoadImageFromMemory(".png", data, (int)size);
  if (!image.data) return 0;
  int ok = image.width >= 2 && image.height >= 1;
  if (ok) {
    Color *pixels = LoadImageColors(image);
    if (pixels) {
      result->width = image.width; result->height = image.height;
      result->first[0] = pixels[0].r; result->first[1] = pixels[0].g;
      result->first[2] = pixels[0].b; result->first[3] = pixels[0].a;
      result->second[0] = pixels[1].r; result->second[1] = pixels[1].g;
      result->second[2] = pixels[1].b; result->second[3] = pixels[1].a;
      result->has_second = 1;
      UnloadImageColors(pixels);
    } else ok = 0;
  }
  UnloadImage(image);
  return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_png_result result;
  (void)parsarium_parse_png(data, size, &result);
  return 0;
}
