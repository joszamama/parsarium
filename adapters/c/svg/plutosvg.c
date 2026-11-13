#include <plutosvg.h>
#include <plutovg.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  plutosvg_document_t *document = plutosvg_document_load_from_file(argv[1], -1, -1);
  if (!document) return 1;
  plutovg_surface_t *surface = plutosvg_document_render_to_surface(document, NULL, -1, -1, NULL, NULL, NULL);
  if (!surface || plutovg_surface_get_width(surface) != 2 || plutovg_surface_get_height(surface) != 1) return 1;
  unsigned char rgba[8] = {0};
  plutovg_convert_argb_to_rgba(rgba, plutovg_surface_get_data(surface), 2, 1,
                               plutovg_surface_get_stride(surface));
  printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
         plutovg_surface_get_width(surface), plutovg_surface_get_height(surface),
         rgba[0], rgba[1], rgba[2], rgba[4], rgba[5], rgba[6]);
  plutovg_surface_destroy(surface);
  plutosvg_document_destroy(document);
  return 0;
}
