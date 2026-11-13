#include <id3tag.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  struct id3_file *file = id3_file_open(argv[1], ID3_FILE_MODE_READONLY);
  if (!file) return 1;
  struct id3_tag *tag = id3_file_tag(file);
  if (!tag) return 1;
  struct id3_frame *title_frame = id3_tag_findframe(tag, ID3_FRAME_TITLE, 0);
  if (!title_frame) return 1;
  union id3_field *text_field = id3_frame_field(title_frame, 1);
  if (!text_field || id3_field_getnstrings(text_field) == 0) return 1;
  const id3_ucs4_t *ucs4 = id3_field_getstrings(text_field, 0);
  if (!ucs4) return 1;
  id3_utf8_t *title = id3_ucs4_utf8duplicate(ucs4);
  if (!title) return 1;
  printf("{\"title\":\"%s\",\"normalized_id3_major\":%u,\"frames\":%u}\n",
         (const char *)title, ID3_TAG_VERSION_MAJOR(id3_tag_version(tag)), tag->nframes);
  free(title);
  id3_file_close(file);
  return 0;
}
