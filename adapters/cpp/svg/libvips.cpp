#include <vips/vips8>
#include <iostream>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  if (VIPS_INIT(argv[0])) return 1;
  try {
    auto image = vips::VImage::svgload(argv[1]);
    auto first = image.getpoint(0, 0);
    auto second = image.getpoint(1, 0);
    if (first.size() < 3 || second.size() < 3) return 1;
    std::cout << "{\"width\":" << image.width() << ",\"height\":" << image.height()
              << ",\"first\":[" << (int)first[0] << ',' << (int)first[1] << ',' << (int)first[2]
              << "],\"second\":[" << (int)second[0] << ',' << (int)second[1] << ',' << (int)second[2]
              << "]}\n";
  } catch (const vips::VError &) {
    return 1;
  }
  vips_shutdown();
  return 0;
}
