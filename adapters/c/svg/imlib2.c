#include <Imlib2.h>
#include <stdint.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  int error = 0;
  Imlib_Image image = imlib_load_image_with_errno_return(argv[1], &error);
  if (!image) return 3;
  imlib_context_set_image(image);
  int width = imlib_image_get_width(), height = imlib_image_get_height();
  const uint32_t *pixels = imlib_image_get_data_for_reading_only();
  if (!pixels || width < 2 || height < 1) return 4;
  printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
         width, height,
         (pixels[0] >> 16) & 255, (pixels[0] >> 8) & 255, pixels[0] & 255,
         (pixels[1] >> 16) & 255, (pixels[1] >> 8) & 255, pixels[1] & 255);
  imlib_free_image();
  return 0;
}
