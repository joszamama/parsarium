#include <mpg123.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  if (mpg123_init() != MPG123_OK) return 1;
  int error = 0;
  mpg123_handle *handle = mpg123_new(NULL, &error);
  if (!handle || mpg123_open(handle, argv[1]) != MPG123_OK) return 1;
  if (mpg123_scan(handle) != MPG123_OK) return 1;
  mpg123_id3v1 *v1 = NULL;
  mpg123_id3v2 *v2 = NULL;
  if (mpg123_id3(handle, &v1, &v2) != MPG123_OK || !v2 || !v2->title) return 1;
  printf("{\"title\":\"%.*s\",\"id3v2_version\":%u}\n",
         (int)v2->title->fill, v2->title->p, v2->version);
  mpg123_close(handle);
  mpg123_delete(handle);
  mpg123_exit();
  return 0;
}
