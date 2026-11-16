#include "harness.h"
#include <unzip.h>
#include <string.h>

int parsarium_parse_zip(const uint8_t *data, size_t size, struct parsarium_zip_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  ZIPFILE state = {0};
  unzFile archive = unzOpen(NULL, (uint8_t *)data, (uint32_t)size, &state,
                            NULL, NULL, NULL, NULL);
  if (!archive) return 0;
  int ok = 0;
  unz_global_info global = {0};
  if (unzGetGlobalInfo(archive, &global) != UNZ_OK || global.number_entry < 1 ||
      unzGoToFirstFile(archive) != UNZ_OK) goto done;
  unz_file_info info = {0};
  if (unzGetCurrentFileInfo(archive, &info, result->name, sizeof(result->name),
                            NULL, 0, NULL, 0) != UNZ_OK ||
      info.uncompressed_size > sizeof(result->content)) goto done;
  result->name_len = strnlen(result->name, sizeof(result->name));
  if (!result->name_len || result->name_len == sizeof(result->name)) goto done;
  if (unzOpenCurrentFile(archive) != UNZ_OK) goto done;
  while (result->content_len < info.uncompressed_size) {
    int n = unzReadCurrentFile(archive, result->content + result->content_len,
                               (unsigned int)(info.uncompressed_size - result->content_len));
    if (n <= 0) break;
    result->content_len += (size_t)n;
  }
  ok = result->content_len == info.uncompressed_size &&
       unzCloseCurrentFile(archive) == UNZ_OK;
  result->entries = global.number_entry;
done:
  unzClose(archive);
  return ok;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_zip_result result;
  (void)parsarium_parse_zip(data, size, &result);
  return 0;
}
