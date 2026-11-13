#include <cairo.h>
#include <stdio.h>
#include <svg-cairo.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  svg_cairo_t *document = NULL;
  if (svg_cairo_create(&document) != SVG_CAIRO_STATUS_SUCCESS) return 1;
  if (svg_cairo_parse(document, argv[1]) != SVG_CAIRO_STATUS_SUCCESS) return 1;
  unsigned int width, height;
  svg_cairo_get_size(document, &width, &height);
  if (width != 2 || height != 1) return 1;
  cairo_surface_t *surface = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, (int)width, (int)height);
  if (cairo_surface_status(surface) != CAIRO_STATUS_SUCCESS) return 1;
  cairo_t *painter = cairo_create(surface);
  if (svg_cairo_render(document, painter) != SVG_CAIRO_STATUS_SUCCESS) return 1;
  cairo_surface_flush(surface);
  unsigned int *pixels = (unsigned int *)cairo_image_surface_get_data(surface);
  unsigned int first = pixels[0], second = pixels[1];
  printf("{\"width\":%u,\"height\":%u,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
         width, height, (first >> 16) & 255, (first >> 8) & 255, first & 255,
         (second >> 16) & 255, (second >> 8) & 255, second & 255);
  cairo_destroy(painter);
  cairo_surface_destroy(surface);
  svg_cairo_destroy(document);
  return 0;
}
