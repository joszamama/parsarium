#include <cairo.h>
#include <librsvg/rsvg.h>
#include <cstdint>
#include <cstring>
#include <iostream>

static void print_rgb(const unsigned char *pixel) {
  std::uint32_t argb;
  std::memcpy(&argb, pixel, sizeof(argb));
  std::cout << '[' << ((argb >> 16) & 255) << ',' << ((argb >> 8) & 255)
            << ',' << (argb & 255) << ']';
}

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  GError *error = nullptr;
  RsvgHandle *handle = rsvg_handle_new_from_file(argv[1], &error);
  if (!handle) return 1;
  double width = 0, height = 0;
  if (!rsvg_handle_get_intrinsic_size_in_pixels(handle, &width, &height)) return 1;
  if (width < 2 || height < 1) return 1;
  cairo_surface_t *surface = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, (int)width, (int)height);
  cairo_t *cr = cairo_create(surface);
  RsvgRectangle viewport = {0, 0, width, height};
  if (!rsvg_handle_render_document(handle, cr, &viewport, &error)) return 1;
  cairo_surface_flush(surface);
  const unsigned char *pixels = cairo_image_surface_get_data(surface);
  std::cout << "{\"width\":" << (int)width << ",\"height\":" << (int)height << ",\"first\":";
  print_rgb(pixels);
  std::cout << ",\"second\":";
  print_rgb(pixels + 4);
  std::cout << "}\n";
  cairo_destroy(cr);
  cairo_surface_destroy(surface);
  g_object_unref(handle);
  return 0;
}
