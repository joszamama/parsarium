#include <lunasvg.h>
#include <iostream>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  auto document = lunasvg::Document::loadFromFile(argv[1]);
  if (!document) return 1;
  auto bitmap = document->renderToBitmap();
  if (bitmap.isNull() || bitmap.width() != 2 || bitmap.height() != 1) return 1;
  bitmap.convertToRGBA();
  const unsigned char *rgba = bitmap.data();
  std::cout << "{\"width\":" << bitmap.width() << ",\"height\":" << bitmap.height()
            << ",\"first\":[" << (unsigned)rgba[0] << ',' << (unsigned)rgba[1]
            << ',' << (unsigned)rgba[2] << "],\"second\":["
            << (unsigned)rgba[4] << ',' << (unsigned)rgba[5] << ','
            << (unsigned)rgba[6] << "]}\n";
  return 0;
}
