#define _GNU_SOURCE
#include "harness.h"
#include <zipc.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parsarium_parse_zip(const uint8_t *data, size_t size, struct parsarium_zip_result *result) {
  if (!data || !result || !size || size > (1u << 20)) return 0;
  memset(result, 0, sizeof(*result));
  char path[] = "/tmp/parsarium-zipc-XXXXXX.zip";
  int fd = mkstemps(path, 4);
  if (fd < 0) return 0;
  size_t written = 0;
  while (written < size) {
    ssize_t n = write(fd, data + written, size - written);
    if (n <= 0) { close(fd); unlink(path); return 0; }
    written += (size_t)n;
  }
  close(fd);
  zipc_t *archive = zipcOpen(path, "r");
  if (!archive) { unlink(path); return 0; }
  zipc_file_t *file = zipcOpenFile(archive, "hello.txt");
  if (!file) { zipcClose(archive); unlink(path); return 0; }
  ssize_t n = 0;
  while (result->content_len < sizeof(result->content) &&
         (n = zipcFileRead(file, result->content + result->content_len,
                           sizeof(result->content) - result->content_len)) > 0)
    result->content_len += (size_t)n;
  int ok = n == 0 && zipcFileFinish(file) >= 0 && zipcClose(archive) >= 0;
  unlink(path);
  if (!ok) return 0;
  return 1;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  struct parsarium_zip_result result;
  (void)parsarium_parse_zip(data, size, &result);
  return 0;
}
