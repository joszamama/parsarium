#include <stdio.h>
#include <vips/vips.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  if (VIPS_INIT(argv[0])) return 1;
  VipsImage *image = NULL;
  if (vips_svgload(argv[1], &image, NULL)) return 1;
  double *first = NULL, *second = NULL;
  int first_n = 0, second_n = 0;
  if (vips_getpoint(image, &first, &first_n, 0, 0, NULL) ||
      vips_getpoint(image, &second, &second_n, 1, 0, NULL) ||
      first_n < 3 || second_n < 3) return 1;
  printf("{\"width\":%d,\"height\":%d,\"first\":[%d,%d,%d],\"second\":[%d,%d,%d]}\n",
         vips_image_get_width(image), vips_image_get_height(image),
         (int)first[0], (int)first[1], (int)first[2],
         (int)second[0], (int)second[1], (int)second[2]);
  g_free(first);
  g_free(second);
  g_object_unref(image);
  vips_shutdown();
  return 0;
}
