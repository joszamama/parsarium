#include "harness.h"
#include <SDL3/SDL.h>
#include <SDL3_image/SDL_image.h>
#include <string.h>

int parsarium_parse_pnm(const uint8_t *data, size_t size, struct parsarium_pnm_result *result) {
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
  int ok = rgba->w >= 1 && rgba->h >= 1;
  if (ok) {
    /* The second pixel is the next one in raster order, if the image has one. */
    const unsigned char *pixels = (const unsigned char *)rgba->pixels;
    const unsigned char *next = rgba->w > 1 ? pixels + 4 : rgba->h > 1 ? pixels + rgba->pitch : NULL;
    result->width = rgba->w; result->height = rgba->h;
    memcpy(result->first, pixels, 4);
    result->has_second = next != NULL;
    if (next) memcpy(result->second, next, 4);
  }
  SDL_DestroySurface(rgba); SDL_Quit();
  return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_pnm_result result;
  (void)parsarium_parse_pnm(data, size, &result);
  return 0;
}
