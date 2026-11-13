#include <stdio.h>
#include <thorvg_capi.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  if (tvg_engine_init(0) != TVG_RESULT_SUCCESS) return 1;
  Tvg_Paint picture = tvg_picture_new();
  if (!picture) return 1;
  if (tvg_picture_load(picture, argv[1]) != TVG_RESULT_SUCCESS) return 1;
  float width, height;
  if (tvg_picture_get_size(picture, &width, &height) != TVG_RESULT_SUCCESS) return 1;
  printf("{\"width\":%.0f,\"height\":%.0f}\n", width, height);
  tvg_paint_rel(picture);
  tvg_engine_term();
  return 0;
}
