#include <id3.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  ID3Tag *tag = ID3Tag_New();
  if (!tag || ID3Tag_LinkWithFlags(tag, argv[1], ID3TT_ID3V2) == 0) return 1;
  ID3Frame *title_frame = ID3Tag_FindFrameWithID(tag, ID3FID_TITLE);
  if (!title_frame) return 1;
  ID3Field *text = ID3Frame_GetField(title_frame, ID3FN_TEXT);
  if (!text) return 1;
  char title[128] = {0};
  if (ID3Field_GetASCII(text, title, sizeof(title)) == 0) return 1;
  printf("{\"title\":\"%s\",\"frames\":%zu}\n", title, ID3Tag_NumFrames(tag));
  ID3Tag_Delete(tag);
  return 0;
}
