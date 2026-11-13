#include <id3v2tag.h>
#include <mpegfile.h>
#include <iostream>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  TagLib::MPEG::File file(argv[1]);
  if (!file.isValid()) return 1;
  TagLib::ID3v2::Tag *tag = file.ID3v2Tag();
  if (!tag) return 1;
  std::cout << "{\"title\":\"" << tag->title().to8Bit(true)
            << "\",\"artist\":\"" << tag->artist().to8Bit(true) << "\"}\n";
  return 0;
}
