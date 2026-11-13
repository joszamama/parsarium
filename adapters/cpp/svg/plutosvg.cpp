#include <plutosvg.h>
#include <plutovg.h>
#include <iostream>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  plutosvg_document_t *document = plutosvg_document_load_from_file(argv[1], -1, -1);
  if (!document) return 1;
  plutovg_surface_t *surface = plutosvg_document_render_to_surface(document, nullptr, -1, -1, nullptr, nullptr, nullptr);
  if (!surface || plutovg_surface_get_width(surface) != 2 || plutovg_surface_get_height(surface) != 1) return 1;
  unsigned char rgba[8] = {0};
  plutovg_convert_argb_to_rgba(rgba, plutovg_surface_get_data(surface), 2, 1,
                               plutovg_surface_get_stride(surface));
  std::cout << "{\"width\":" << plutovg_surface_get_width(surface)
            << ",\"height\":" << plutovg_surface_get_height(surface)
            << ",\"first\":[" << (unsigned)rgba[0] << ',' << (unsigned)rgba[1]
            << ',' << (unsigned)rgba[2] << "],\"second\":["
            << (unsigned)rgba[4] << ',' << (unsigned)rgba[5] << ','
            << (unsigned)rgba[6] << "]}\n";
  plutovg_surface_destroy(surface);
  plutosvg_document_destroy(document);
  return 0;
}
