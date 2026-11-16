#include "harness.h"
#include <gsf/gsf.h>
#include <string.h>

int parsarium_parse_zip(const uint8_t *data, size_t size, struct parsarium_zip_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  gsf_init();
  GsfInput *input = gsf_input_memory_new((const guint8 *)data, size, FALSE);
  if (!input) { gsf_shutdown(); return 0; }
  GError *error = NULL;
  GsfInfile *archive = gsf_infile_zip_new(input, &error);
  if (error) { g_error_free(error); error = NULL; }
  if (!archive) { g_object_unref(input); gsf_shutdown(); return 0; }
  int ok = 0;
  int count = gsf_infile_num_children(archive);
  if (count > 0) {
    const char *name = gsf_infile_name_by_index(archive, 0);
    GsfInput *entry = gsf_infile_child_by_index(archive, 0);
    if (name && entry) {
      result->name_len = strnlen(name, sizeof(result->name));
      gsf_off_t content_size = gsf_input_size(entry);
      if (result->name_len && result->name_len < sizeof(result->name) &&
          content_size >= 0 && content_size <= (gsf_off_t)sizeof(result->content)) {
        memcpy(result->name, name, result->name_len);
        const guint8 *contents = gsf_input_read(entry, (size_t)content_size, NULL);
        if (contents) {
          memcpy(result->content, contents, (size_t)content_size);
          result->content_len = (size_t)content_size;
          result->entries = count;
          ok = 1;
        }
      }
    }
    if (entry) g_object_unref(entry);
  }
  g_object_unref(archive);
  g_object_unref(input);
  gsf_shutdown();
  return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_zip_result result;
  (void)parsarium_parse_zip(data, size, &result);
  return 0;
}
