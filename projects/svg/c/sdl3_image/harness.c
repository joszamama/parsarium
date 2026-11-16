#include "harness.h"
#include <SDL3/SDL.h>
#include <SDL3_image/SDL_image.h>
#include <string.h>

int parsarium_parse_svg(const uint8_t *data, size_t size, struct parsarium_svg_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  if (!SDL_Init(0)) return 0;
  SDL_IOStream *input = SDL_IOFromConstMem(data, size);
  if (!input) { SDL_Quit(); return 0; }
  SDL_Surface *decoded = IMG_Load_IO(input, true);
  if (!decoded) { SDL_Quit(); return 0; }
  SDL_Surface *rgba = SDL_ConvertSurface(decoded, SDL_PIXELFORMAT_RGBA32);
  SDL_DestroySurface(decoded);
  if (!rgba) { SDL_Quit(); return 0; }
  int ok = rgba->w >= 2 && rgba->h >= 1 && rgba->pitch >= 8;
  if (ok) {
    const unsigned char *pixels = (const unsigned char *)rgba->pixels;
    result->width = rgba->w; result->height = rgba->h;
    memcpy(result->first, pixels, 4);
    memcpy(result->second, pixels + 4, 4);
    result->has_second = 1;
  }
  SDL_DestroySurface(rgba); SDL_Quit();
  return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_svg_result result;
  (void)parsarium_parse_svg(data, size, &result);
  return 0;
}
