#include <cairo.h>
#include <librsvg/rsvg.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static void print_rgb(const unsigned char *pixel) {
  uint32_t argb;
  memcpy(&argb, pixel, sizeof(argb));
  printf("[%u,%u,%u]", (argb >> 16) & 255, (argb >> 8) & 255, argb & 255);
}

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  GError *error = NULL;
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
  printf("{\"width\":%d,\"height\":%d,\"first\":", (int)width, (int)height);
  print_rgb(pixels);
  printf(",\"second\":");
  print_rgb(pixels + 4);
  printf("}\n");
  cairo_destroy(cr);
  cairo_surface_destroy(surface);
  g_object_unref(handle);
  return 0;
}
