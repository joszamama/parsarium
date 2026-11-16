#include "harness.h"
#include <archive.h>
#include <archive_entry.h>
#include <string.h>

int parsarium_parse_zip(const uint8_t *data, size_t size, struct parsarium_zip_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  struct archive *reader = archive_read_new();
  if (!reader) return 0;
  int ok = 0, status;
  struct archive_entry *entry = NULL;
  if (archive_read_support_format_zip(reader) != ARCHIVE_OK ||
      archive_read_open_memory(reader, data, size) != ARCHIVE_OK) goto done;
  while ((status = archive_read_next_header(reader, &entry)) == ARCHIVE_OK) {
    result->entries++;
    if (result->entries == 1) {
      const char *name = archive_entry_pathname(entry);
      if (!name) goto done;
      result->name_len = strnlen(name, sizeof(result->name));
      if (!result->name_len || result->name_len == sizeof(result->name)) goto done;
      memcpy(result->name, name, result->name_len);
      la_ssize_t n;
      while (result->content_len < sizeof(result->content) &&
             (n = archive_read_data(reader, result->content + result->content_len,
                                    sizeof(result->content) - result->content_len)) > 0)
        result->content_len += (size_t)n;
      if (n < 0) goto done;
    }
  }
  ok = status == ARCHIVE_EOF && result->entries > 0;
done:
  archive_read_free(reader);
  return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_zip_result result;
  (void)parsarium_parse_zip(data, size, &result);
  return 0;
}
