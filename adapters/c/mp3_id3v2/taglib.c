#include <stdio.h>
#include <tag_c.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  TagLib_File *file = taglib_file_new_type(argv[1], TagLib_File_MPEG);
  if (!file || !taglib_file_is_valid(file)) return 1;
  TagLib_Tag *tag = taglib_file_tag(file);
  if (!tag) return 1;
  char *title = taglib_tag_title(tag);
  char *artist = taglib_tag_artist(tag);
  if (!title || !artist) return 1;
  printf("{\"title\":\"%s\",\"artist\":\"%s\"}\n", title, artist);
  taglib_tag_free_strings();
  taglib_file_free(file);
  return 0;
}
