#include <thorvg.h>
#include <iostream>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  if (tvg::Initializer::init(0) != tvg::Result::Success) return 1;
  tvg::Picture *picture = tvg::Picture::gen();
  if (!picture) return 1;
  if (picture->load(argv[1]) != tvg::Result::Success) return 1;
  float width, height;
  if (picture->size(&width, &height) != tvg::Result::Success) return 1;
  std::cout << "{\"width\":" << width << ",\"height\":" << height << "}\n";
  picture->unref(true);
  tvg::Initializer::term();
  return 0;
}
