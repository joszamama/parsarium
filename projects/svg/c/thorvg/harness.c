#include "harness.h"
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <thorvg_capi.h>

#define PARSARIUM_MAX_SIDE 4096.0f

static void rgb(uint32_t pixel, unsigned char out[3]) {
  out[0] = (pixel >> 16) & 0xff;
  out[1] = (pixel >> 8) & 0xff;
  out[2] = pixel & 0xff;
}

int parsarium_parse_svg(const uint8_t *data, size_t size, struct parsarium_svg_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  if (tvg_engine_init(0) != TVG_RESULT_SUCCESS) return 0;
  int ok = 0;
  uint32_t *pixels = NULL;
  Tvg_Canvas canvas = NULL;
  Tvg_Paint picture = tvg_picture_new();
  float fw = 0, fh = 0;
  /* copy=true: ThorVG caches borrowed data by address, which would reuse a stale parse across inputs. */
  if (!picture || tvg_picture_load_data(picture, (const char *)data, (uint32_t)size, "svg", NULL, true) != TVG_RESULT_SUCCESS) goto done;
  if (tvg_picture_get_size(picture, &fw, &fh) != TVG_RESULT_SUCCESS) goto done;
  if (!isfinite(fw) || !isfinite(fh) || fw < 1.0f || fh < 1.0f || fw > PARSARIUM_MAX_SIDE || fh > PARSARIUM_MAX_SIDE) goto done;
  unsigned w = (unsigned)lroundf(fw), h = (unsigned)lroundf(fh);
  pixels = calloc((size_t)w * h, sizeof(*pixels));
  canvas = tvg_swcanvas_create(TVG_ENGINE_OPTION_DEFAULT);
  if (!pixels || !canvas) goto done;
  if (tvg_swcanvas_set_target(canvas, pixels, w, w, h, TVG_COLORSPACE_ARGB8888S) != TVG_RESULT_SUCCESS) goto done;
  if (tvg_canvas_add(canvas, picture) != TVG_RESULT_SUCCESS) goto done;
  picture = NULL; /* owned by the canvas */
  if (tvg_canvas_draw(canvas, true) != TVG_RESULT_SUCCESS || tvg_canvas_sync(canvas) != TVG_RESULT_SUCCESS) goto done;
  result->width = w;
  result->height = h;
  rgb(pixels[0], result->first);
  if (w > 1) {
    rgb(pixels[w - 1], result->second);
    result->has_second = 1;
  }
  ok = 1;
done:
  if (canvas) tvg_canvas_destroy(canvas);
  if (picture) tvg_paint_rel(picture);
  free(pixels);
  tvg_engine_term();
  return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_svg_result result;
  (void)parsarium_parse_svg(data, size, &result);
  return 0;
}
