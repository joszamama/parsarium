#include "harness.h"
#include <SDL.h>
#include <SDL_image.h>
#include <stdio.h>
#include <string.h>

/* SDL reports why a call failed through SDL_GetError(); it is copied before SDL_Quit(). */
static char last_error[256];
const char *parsarium_pnm_error(void) { return last_error; }
static void keep_error(const char *call) {
  const char *reason = SDL_GetError();
  snprintf(last_error, sizeof(last_error), "%s failed: %s", call, reason ? reason : "");
}

int parsarium_parse_pnm(const uint8_t *data, size_t size, struct parsarium_pnm_result *result) {
  last_error[0] = 0;
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  if (SDL_Init(0) != 0) return 0;
  SDL_RWops *input = SDL_RWFromConstMem(data, (int)size);
  if (!input) { SDL_Quit(); return 0; }
  SDL_Surface *decoded = IMG_Load_RW(input, 1);
  if (!decoded) { keep_error("IMG_Load_RW"); SDL_Quit(); return 0; }
  SDL_Surface *rgba = SDL_ConvertSurfaceFormat(decoded, SDL_PIXELFORMAT_RGBA32, 0);
  SDL_FreeSurface(decoded);
  if (!rgba) { keep_error("SDL_ConvertSurfaceFormat"); SDL_Quit(); return 0; }
  int ok = rgba->w >= 1 && rgba->h >= 1;
  if (!ok) snprintf(last_error, sizeof(last_error), "decoded surface has no pixels (%dx%d)", rgba->w, rgba->h);
  if (ok) {
    /* The second pixel is the next one in raster order, if the image has one. */
    const unsigned char *pixels = (const unsigned char *)rgba->pixels;
    const unsigned char *next = rgba->w > 1 ? pixels + 4 : rgba->h > 1 ? pixels + rgba->pitch : NULL;
    result->width = rgba->w; result->height = rgba->h;
    memcpy(result->first, pixels, 4);
    result->has_second = next != NULL;
    if (next) memcpy(result->second, next, 4);
  }
  SDL_FreeSurface(rgba); SDL_Quit();
  return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_pnm_result result;
  (void)parsarium_parse_pnm(data, size, &result);
  return 0;
}
