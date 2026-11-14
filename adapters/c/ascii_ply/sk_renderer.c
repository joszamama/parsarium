/* The released sk_renderer package documents micro_ply as a standalone tool. */
#define MICRO_PLY_IMPL
#include "micro_ply.h"

#include <stdio.h>

int main(int argc, char **argv)
{
  if (argc != 2) return 2;
  FILE *input = fopen(argv[1], "rb");
  if (!input) return 3;
  if (fseek(input, 0, SEEK_END)) return 4;
  long length = ftell(input);
  if (length <= 0 || fseek(input, 0, SEEK_SET)) return 5;
  void *bytes = malloc((size_t)length);
  if (!bytes || fread(bytes, 1, (size_t)length, input) != (size_t)length)
    return 6;
  fclose(input);

  ply_file_t ply = {0};
  if (!ply_read(bytes, (size_t)length, &ply)) return 7;
  int vertices = -1, faces = -1;
  for (int i = 0; i < ply.count; i++) {
    if (!strcmp(ply.elements[i].name, PLY_ELEMENT_VERTICES))
      vertices = ply.elements[i].count;
    if (!strcmp(ply.elements[i].name, PLY_ELEMENT_FACES))
      faces = ply.elements[i].count;
  }

  float zero = 0.0f;
  ply_map_t map[] = {
    {PLY_PROP_POSITION_X, ply_prop_decimal, sizeof(float), 0, &zero},
    {PLY_PROP_POSITION_Y, ply_prop_decimal, sizeof(float), 4, &zero},
    {PLY_PROP_POSITION_Z, ply_prop_decimal, sizeof(float), 8, &zero},
  };
  float *positions = NULL;
  int32_t converted = 0;
  ply_convert(&ply, PLY_ELEMENT_VERTICES, map, 3, 3 * sizeof(float),
              (void **)&positions, &converted);
  if (!positions || converted < 2) return 8;
  printf("{\"vertices\":%d,\"faces\":%d,\"converted\":%d,"
         "\"second_x\":%.1f}\n",
         vertices, faces, converted, positions[3]);
  free(positions);
  ply_free(&ply);
  free(bytes);
  return 0;
}
