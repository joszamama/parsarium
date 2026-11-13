#include <glycin.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int rgb(const unsigned char *pixel, GlyMemoryFormat format, unsigned char out[3]) {
  switch (format) {
    case GLY_MEMORY_B8G8R8A8_PREMULTIPLIED:
    case GLY_MEMORY_B8G8R8A8:
    case GLY_MEMORY_B8G8R8:
      out[0] = pixel[2]; out[1] = pixel[1]; out[2] = pixel[0]; return 1;
    case GLY_MEMORY_R8G8B8A8_PREMULTIPLIED:
    case GLY_MEMORY_R8G8B8A8:
    case GLY_MEMORY_R8G8B8:
      out[0] = pixel[0]; out[1] = pixel[1]; out[2] = pixel[2]; return 1;
    default:
      return 0;
  }
}

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  GFile *file = g_file_new_for_path(argv[1]);
  GlyLoader *loader = gly_loader_new(file);
  GError *error = NULL;
  GlyImage *image = gly_loader_load(loader, &error);
  if (!image) { fprintf(stderr, "load: %s\n", error ? error->message : "unknown"); return 3; }
  GlyFrame *frame = gly_image_next_frame(image, &error);
  if (!frame) { fprintf(stderr, "frame: %s\n", error ? error->message : "unknown"); return 4; }
  uint32_t width = gly_frame_get_width(frame), height = gly_frame_get_height(frame);
  uint32_t stride = gly_frame_get_stride(frame);
  GlyMemoryFormat format = gly_frame_get_memory_format(frame);
  GBytes *bytes = gly_frame_get_buf_bytes(frame);
  gsize length = 0;
  const unsigned char *data = g_bytes_get_data(bytes, &length);
  if (!data || width != 2 || height != 1 || stride < 6 || length < stride) return 5;
  const unsigned int channels = (format == GLY_MEMORY_R8G8B8 || format == GLY_MEMORY_B8G8R8) ? 3 : 4;
  if (stride < 2 * channels) return 6;
  unsigned char first[3], second[3];
  if (!rgb(data, format, first) || !rgb(data + channels, format, second)) return 7;
  const char *mime = gly_image_get_mime_type(image);
  if (!mime || strcmp(mime, "image/svg+xml") != 0) return 8;
  printf("{\"width\":%u,\"height\":%u,\"mime\":\"%s\",\"first\":[%u,%u,%u],\"second\":[%u,%u,%u]}\n",
         width, height, mime, first[0], first[1], first[2], second[0], second[1], second[2]);
  g_object_unref(frame);
  g_object_unref(image);
  g_object_unref(loader);
  g_object_unref(file);
  return 0;
}
