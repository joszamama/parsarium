#include <id3/tag.h>
#include <id3/id3lib_frame.h>
#include <id3/field.h>
#include <iostream>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  ID3_Tag tag;
  if (tag.Link(argv[1], ID3TT_ID3V2) == 0) return 1;
  ID3_Frame *title_frame = tag.Find(ID3FID_TITLE);
  if (!title_frame) return 1;
  ID3_Field *text = title_frame->GetField(ID3FN_TEXT);
  if (!text) return 1;
  char title[128] = {0};
  if (text->Get(title, sizeof(title)) == 0) return 1;
  std::cout << "{\"title\":\"" << title << "\",\"frames\":" << tag.NumFrames() << "}\n";
  return 0;
}
