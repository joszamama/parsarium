#include <stdio.h>
#include <svg.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  svg_t *document = NULL;
  if (svg_create(&document) != SVG_STATUS_SUCCESS) return 1;
  if (svg_parse(document, argv[1]) != SVG_STATUS_SUCCESS) return 1;
  svg_length_t width, height;
  svg_get_size(document, &width, &height);
  if (width.unit != SVG_LENGTH_UNIT_PX || height.unit != SVG_LENGTH_UNIT_PX) return 1;
  printf("{\"width\":%.0f,\"height\":%.0f}\n", width.value, height.value);
  svg_destroy(document);
  return 0;
}
