#include <Evas.h>
#include <stdint.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  if (evas_init() <= 0) return 3;
  Evas *evas = evas_new();
  int method = evas_render_method_lookup("buffer");
  if (!evas || method < 0) return 4;
  evas_output_method_set(evas, method);
  evas_output_size_set(evas, 2, 1);
  evas_output_viewport_set(evas, 0, 0, 2, 1);
  Evas_Object *image = evas_object_image_add(evas);
  evas_object_image_file_set(image, argv[1], NULL);
  if (evas_object_image_load_error_get(image) != EVAS_LOAD_ERROR_NONE) return 5;
  int width = 0, height = 0;
  evas_object_image_size_get(image, &width, &height);
  const uint32_t *pixels = evas_object_image_data_get(image, EINA_FALSE);
  if (!pixels || width < 2 || height < 1) return 6;
  printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
         width, height,
         (pixels[0] >> 16) & 255, (pixels[0] >> 8) & 255, pixels[0] & 255,
         (pixels[1] >> 16) & 255, (pixels[1] >> 8) & 255, pixels[1] & 255);
  evas_object_del(image);
  evas_free(evas);
  evas_shutdown();
  return 0;
}
