#include <stdio.h>
#include <vips/vips.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  if (VIPS_INIT(argv[0])) return 1;
  VipsImage *image = NULL;
  if (vips_pdfload(argv[1], &image, NULL)) {
    vips_shutdown();
    return 1;
  }
  int pages = 0;
  if (vips_image_get_int(image, "n-pages", &pages)) {
    g_object_unref(image);
    vips_shutdown();
    return 1;
  }
  printf("{\"pages\":%d,\"width\":%d,\"height\":%d}\n",
         pages, vips_image_get_width(image), vips_image_get_height(image));
  g_object_unref(image);
  vips_shutdown();
  return 0;
}
