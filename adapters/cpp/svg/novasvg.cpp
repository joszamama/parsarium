#include <cmath>
#include <novasvg/novasvg.h>
#include <cstdio>

int main(int argc, char** argv) {
  if (argc != 2) return 2;
  auto document = novasvg::Document::loadFromFile(argv[1]);
  if (!document) return 1;
  auto rectangles = document->querySelectorAll("rect");
  std::printf("{\"width\":%.0f,\"height\":%.0f,\"rectangles\":%zu}\n",
              document->width(), document->height(), rectangles.size());
  return 0;
}
