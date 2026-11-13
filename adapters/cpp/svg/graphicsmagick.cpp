#include <Magick++.h>
#include <cmath>
#include <iostream>

static void print_rgb(const Magick::ColorRGB &color) {
  std::cout << '[' << std::lround(color.red() * 255) << ','
            << std::lround(color.green() * 255) << ','
            << std::lround(color.blue() * 255) << ']';
}

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  try {
    Magick::InitializeMagick(argv[0]);
    Magick::Image image(argv[1]);
    std::cout << "{\"width\":" << image.columns() << ",\"height\":" << image.rows()
              << ",\"first\":";
    print_rgb(Magick::ColorRGB(image.pixelColor(0, 0)));
    std::cout << ",\"second\":";
    print_rgb(Magick::ColorRGB(image.pixelColor(1, 0)));
    std::cout << "}\n";
    return 0;
  } catch (const std::exception &error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
