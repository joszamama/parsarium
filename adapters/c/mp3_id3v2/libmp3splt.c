#ifdef __cplusplus
extern "C" {
#endif
#include <mp3splt.h>
#ifdef __cplusplus
}
#endif
#include <stdio.h>

struct output_state {
  size_t bytes;
  unsigned char first[4];
  size_t first_length;
};

static void on_write(const void *ptr, size_t size, size_t nmemb, void *ctx) {
  struct output_state *out = (struct output_state *)ctx;
  const unsigned char *data = (const unsigned char *)ptr;
  size_t length = size * nmemb;
  for (size_t i = 0; i < length && out->first_length < 4; i++)
    out->first[out->first_length++] = data[i];
  out->bytes += length;
}

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  splt_code error = SPLT_OK;
  splt_state *state = mp3splt_new_state(&error);
  if (!state) return 1;
  struct output_state out = {0, {0}, 0};
  if (mp3splt_find_plugins(state) != SPLT_OK ||
      mp3splt_set_filename_to_split(state, argv[1]) != SPLT_OK ||
      mp3splt_set_int_option(state, SPLT_OPT_PRETEND_TO_SPLIT, SPLT_TRUE) != SPLT_OK ||
      mp3splt_set_pretend_to_split_write_function(state, on_write, &out) != SPLT_OK) return 1;
  splt_point *start = mp3splt_point_new(0, &error);
  splt_point *end = mp3splt_point_new(50, &error);
  if (!start || !end ||
      mp3splt_append_splitpoint(state, start) != SPLT_OK ||
      mp3splt_append_splitpoint(state, end) != SPLT_OK) return 1;
  splt_code result = mp3splt_split(state);
  if (result != SPLT_OK_SPLIT || out.first_length != 4 || out.bytes == 0) return 1;
  printf("{\"split_status\":%d,\"segment_bytes\":%zu,\"frame_header\":\"%02x%02x%02x%02x\"}\n",
         result, out.bytes, out.first[0], out.first[1], out.first[2], out.first[3]);
  mp3splt_free_state(state);
  return 0;
}
