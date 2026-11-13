#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <svgtiny.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  FILE *file = fopen(argv[1], "rb");
  if (!file) return 1;
  if (fseek(file, 0, SEEK_END) != 0) return 1;
  long length = ftell(file);
  if (length < 0 || fseek(file, 0, SEEK_SET) != 0) return 1;
  char *bytes = malloc((size_t)length);
  if (!bytes) return 1;
  if (fread(bytes, 1, (size_t)length, file) != (size_t)length) return 1;
  fclose(file);

  struct svgtiny_diagram *diagram = svgtiny_create();
  if (!diagram) return 1;
  svgtiny_code status = svgtiny_parse(diagram, bytes, (size_t)length, argv[1], 2, 1);
  free(bytes);
  if (status != svgtiny_OK || diagram->shape_count != 2) return 1;
  svgtiny_colour first = diagram->shape[0].fill;
  svgtiny_colour second = diagram->shape[1].fill;
  printf("{\"width\":%d,\"height\":%d,\"shapes\":%u,\"first\":[%d,%d,%d],\"second\":[%d,%d,%d]}\n",
         diagram->width, diagram->height, diagram->shape_count,
         svgtiny_RED(first), svgtiny_GREEN(first), svgtiny_BLUE(first),
         svgtiny_RED(second), svgtiny_GREEN(second), svgtiny_BLUE(second));
  svgtiny_free(diagram);
  return 0;
}
